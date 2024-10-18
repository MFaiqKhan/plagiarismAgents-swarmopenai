import requests
import os
import time
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.utils.logging_config import logger

API_URL = "http://localhost:8000/upload"

def upload_document(file_path: str):
    """
    Uploads a document to the FastAPI server for plagiarism detection.

    :param file_path: Path to the document to upload.
    :return: Response from the server.
    """
    logger.info(f"Uploading document: {file_path}")
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f, 'text/plain')}
        response = requests.post(API_URL, files=files)
    logger.info(f"Upload response: {response.json()}")
    return response.json()

def main():
    document_path = input("Enter the path to the document you want to upload: ").strip()
    if not os.path.exists(document_path):
        logger.error("File does not exist.")
        return
    
    response = upload_document(document_path)
    if response.get("document_id"):
        document_id = response["document_id"]
        logger.info(f"Document uploaded successfully. Document ID: {document_id}")
        print(f"Document uploaded successfully. Document ID: {document_id}")
        print("Processing document for plagiarism detection...")
        
        # Polling for status
        status_url = f"http://localhost:8000/status/{document_id}"
        report_url = f"http://localhost:8000/report/{document_id}"
        
        while True:
            try:
                status_response = requests.get(status_url).json()
                if status_response["status"] == "completed":
                    print("Processing completed.")
                    break
                elif status_response["status"] == "processing":
                    print("Still processing... Waiting for 5 seconds.")
                    time.sleep(5)
                else:
                    print("Unknown status received.")
                    break
            except Exception as e:
                print(f"Error checking status: {e}")
                return
        
        # Retrieve the report
        try:
            report_response = requests.get(report_url)
            if report_response.status_code == 200:
                logger.info(f"Retrieved plagiarism report for Document ID {document_id}")
                print(f"\nPlagiarism Report for Document ID {document_id}:\n")
                print(report_response.text)
            else:
                logger.error("Failed to retrieve the report.")
        except Exception as e:
            logger.exception(f"Error fetching report: {e}")
    else:
        logger.error(f"Failed to upload document. Response: {response}")

if __name__ == "__main__":
    main()
