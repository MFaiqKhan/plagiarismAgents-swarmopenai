import os
import uuid
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import PlainTextResponse
from swarm import Swarm
from backend.app.database.file_reports import get_report
from backend.app.processors.document_processor import process_document_for_plagiarism
import aiofiles
import openai
from backend.app.utils.logging_config import logger

# Load environment variables from .env file
load_dotenv()

# After load_dotenv()
#print(f"OpenAI API Keyyyy: {os.getenv('OPENAI_API_KEY')}")

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')  # Ensure this environment variable is set

# Configuration Settings
REPORTS_PATH = os.getenv('REPORTS_PATH', 'reports')
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 1048576))  # Default to 1MB
ALLOWED_CONTENT_TYPES = os.getenv('ALLOWED_CONTENT_TYPES', 'text/plain').split(',')
LOG_FILE = os.getenv('LOG_FILE', 'E:/Github/swarm-openai/app.log')

app = FastAPI()
swarm = Swarm()

# Ensure the reports directory exists at startup
os.makedirs(REPORTS_PATH, exist_ok=True)

@app.post("/upload", summary="Upload a document for plagiarism detection")
async def upload_document(file: UploadFile = File(...), *,background_tasks: BackgroundTasks):
    """
    Upload a document for plagiarism detection.

    - **file**: The file to be uploaded. Must be a plain text file and not exceed the maximum allowed size.
    - **background_tasks**: Handles asynchronous processing of the uploaded document.
    
    Returns a confirmation message with a unique document ID.
    """
    # Input Validation
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        logger.warning(f"Unsupported file type: {file.content_type}")
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed types: {ALLOWED_CONTENT_TYPES}")
    
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        logger.warning(f"File size exceeded: {len(contents)} bytes")
        raise HTTPException(status_code=400, detail=f"File size exceeds the limit of {MAX_FILE_SIZE} bytes.")
    
    try:
        # Generate a unique document ID
        document_id = str(uuid.uuid4())
        
        # Define the file path
        file_path = os.path.join(REPORTS_PATH, f"{document_id}_target.txt")
        
        # Asynchronously save the uploaded file
        async with aiofiles.open(file_path, 'wb') as out_file:
            await out_file.write(contents)
            logger.info(f"Saved uploaded file to {file_path}")
        
        # Add a background task to process the document for plagiarism
        background_tasks.add_task(process_document_for_plagiarism, document_id)
        logger.info(f"Started plagiarism processing for document ID {document_id}")
        
        return {"message": "Document uploaded successfully.", "document_id": document_id}
    
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload document.")

@app.get("/status/{document_id}", summary="Check the processing status of a document")
async def check_status(document_id: str):
    """
    Check the processing status of a document.

    - **document_id**: The unique identifier of the document.

    Returns the status of the document processing.
    """
    try:
        report_file = os.path.join(REPORTS_PATH, f"{document_id}_report.txt")
        status = "completed" if os.path.exists(report_file) else "processing"
        logger.info(f"Checked status for document ID {document_id}: {status}")
        return {"status": status, "document_id": document_id}
    except Exception as e:
        logger.error(f"Error checking status for document ID {document_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to check document status.")

@app.get("/report/{document_id}", response_class=PlainTextResponse, summary="Retrieve the plagiarism report for a document")
def fetch_report(document_id: str):
    """
    Retrieve the plagiarism report for a given document ID.

    - **document_id**: The unique identifier of the document.

    Returns the content of the plagiarism report.
    """
    try:
        report_content = get_report(document_id)
        if not report_content:
            logger.warning(f"Report not found for document ID {document_id}")
            raise HTTPException(status_code=404, detail="Report not found.")
        logger.info(f"Fetched report for document ID {document_id}")
        return report_content
    except Exception as e:
        logger.error(f"Error fetching report for document ID {document_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch report.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
