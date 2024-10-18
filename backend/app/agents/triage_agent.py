from swarm import Agent, Result
from typing import List, Dict
from backend.app.agents.rabin_karp import rabin_karp_plagiarism
from backend.app.utils.logging_config import logger

def analyze_section_plagiarism(section_text: str, n: int = 5) -> str:
    logger.info(f"Analyzing section for plagiarism (first 50 chars): {section_text[:50]}...")
    plagiarism_instances = rabin_karp_plagiarism(section_text, n)
    logger.info(f"Plagiarism instances found: {len(plagiarism_instances)}")

    if plagiarism_instances:
        summary = f"Plagiarism detected in {len(plagiarism_instances)} instances."
        details = "\n".join([
            f"Source Document: {instance['source_document']} | "
            f"Position: {instance['position_in_target']} | "
            f"N-gram: \"{instance['ngram']}\""
            for instance in plagiarism_instances
        ])
        full_report = f"{summary}\nDetails:\n{details}"
        logger.info(f"Plagiarism report generated: {summary}")
    else:
        full_report = "No plagiarism detected in this section."
        logger.info("No plagiarism detected in this section.")

    return full_report

def analyze_introduction(text: str) -> str:
    logger.info("Analyzing Introduction section")
    return analyze_section_plagiarism(text)

def analyze_body(text: str) -> str:
    logger.info("Analyzing Body section")
    return analyze_section_plagiarism(text)

def analyze_conclusion(text: str) -> str:
    logger.info("Analyzing Conclusion section")
    return analyze_section_plagiarism(text)

# Define Specialized Plagiarism Agents
introduction_agent = Agent(
    name="Introduction Plagiarism Agent",
    instructions="""
        You are an Introduction Plagiarism Agent responsible for analyzing the introduction section of a document.
        Identify any instances of plagiarism by comparing the section text against known source documents.
    """,
    functions=[analyze_introduction],
)

body_agent = Agent(
    name="Body Plagiarism Agent",
    instructions="""
        You are a Body Plagiarism Agent responsible for analyzing the main body of a document.
        Identify any instances of plagiarism by comparing the section text against known source documents.
    """,
    functions=[analyze_body],
)

conclusion_agent = Agent(
    name="Conclusion Plagiarism Agent",
    instructions="""
        You are a Conclusion Plagiarism Agent responsible for analyzing the conclusion section of a document.
        Identify any instances of plagiarism by comparing the section text against known source documents.
    """,
    functions=[analyze_conclusion],
)

# Define Triage Agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are a Triage Agent responsible for determining which section of a document to analyze for plagiarism.
    Based on the content provided, decide whether it's an introduction, body, or conclusion, and then perform the appropriate analysis.
    Use the available functions to analyze the respective sections in the order: introduction, body, conclusion.
    """,
    functions=[
        analyze_introduction,
        analyze_body,
        analyze_conclusion
    ],
    model="gpt-4o"
)
