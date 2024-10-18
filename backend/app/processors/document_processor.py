from typing import Dict
from backend.app.agents.triage_agent import triage_agent
from swarm import Swarm
import os
import logging
from dotenv import load_dotenv
import openai
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"), 
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

logger.info("Starting document processor module")

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
logger.info(f"Loading .env file from: {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path)

# After load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    logger.info(f"OpenAI API Key loaded: {'*' * (len(api_key) - 4) + api_key[-4:]}")
else:
    logger.error("OPENAI_API_KEY not found in environment variables")
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize OpenAI client
logger.info("Initializing OpenAI client")
client = openai.OpenAI(api_key=api_key)

# Initialize Swarm client
logger.info("Initializing Swarm client")
swarm = Swarm(client)

def split_into_sections(content: str) -> Dict[str, str]:
    logger.info("Splitting document into sections")
    sections = {}
    current_section = "Introduction"  # Default section
    sections[current_section] = ""

    for line in content.split('\n'):
        line = line.strip()
        if line.lower().startswith("introduction"):
            current_section = "Introduction"
            sections[current_section] = ""
        elif line.lower().startswith("body"):
            current_section = "Body"
            sections[current_section] = ""
        elif line.lower().startswith("conclusion"):
            current_section = "Conclusion"
            sections[current_section] = ""
        else:
            if current_section not in sections:
                sections[current_section] = ""
            sections[current_section] += " " + line

    logger.debug(f"Document split into {len(sections)} sections: {', '.join(sections.keys())}")
    return sections

def process_document_for_plagiarism(document_id: str):
    logger.info(f"Starting plagiarism processing for document ID: {document_id}")
    try:
        # Define paths
        REPORTS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'reports')
        logger.debug(f"Reports path: {REPORTS_PATH}")

        # Path to the target document
        target_file_path = os.path.join(REPORTS_PATH, f"{document_id}_target.txt")
        logger.debug(f"Target file path: {target_file_path}")

        # Read the target document
        try:
            with open(target_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.debug(f"Content length of uploaded document: {len(content)} characters")
            logger.debug(f"First 100 characters of content: {content[:100]}")
            logger.info(f"Successfully read target document: {document_id}")
            logger.debug(f"Document content length: {len(content)} characters")
        except FileNotFoundError:
            logger.error(f"Target document {document_id} not found at {target_file_path}")
            return
        except Exception as e:
            logger.exception(f"Unexpected error reading target document {document_id}: {e}")
            return

        # Split document into sections
        sections = split_into_sections(content)

        # Run the triage_agent to determine sections to analyze
        logger.info("Running triage agent")
        try:
            response = swarm.run(
                agent=triage_agent,
                messages=[{"role": "user", "content": content}],
                max_turns=1
            )
            logger.debug(f"Triage agent response: {response}")
            
            # Extract the report from the response
            aggregated_report = ""
            for message in response.messages:
                if message['role'] == 'tool':
                    aggregated_report += f"{message['tool_name']} result:\n{message['content']}\n\n"
            
            logger.info("Extracted aggregated report from triage agent response")
            logger.debug(f"Aggregated report:\n{aggregated_report}")
            
            # Save the aggregated report to the reports folder
            report_file_path = os.path.join(REPORTS_PATH, f"{document_id}_report.txt")
            logger.debug(f"Saving report to: {report_file_path}")
            try:
                with open(report_file_path, 'w', encoding='utf-8') as f:
                    f.write(aggregated_report)
                logger.info(f"Plagiarism report saved for document ID: {document_id}")
            except Exception as e:
                logger.exception(f"Error saving plagiarism report for document ID {document_id}: {e}")

            logger.info(f"Plagiarism processing completed for document ID: {document_id}")
        except Exception as e:
            logger.exception(f"Error running triage_agent: {e}")
            return
    except Exception as e:
        logger.exception(f"Error processing document {document_id}: {e}")
        raise

if __name__ == "__main__":
    logger.info("Document processor module run directly")
