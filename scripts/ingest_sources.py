import sys
import os
from backend.app.utils.logging_config import logger

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from backend.app.database.file_ingest import ingest_source_document

def read_source_files(source_folder):
    source_docs = []
    if not os.path.exists(source_folder):
        logger.error(f"The directory {source_folder} does not exist.")
        return source_docs

    for file_name in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                source_docs.append((file_name, content))
                logger.info(f"Read source file: {file_name}")
    return source_docs

def main():
    logger.info("Starting source document ingestion")
    source_folder = os.path.join(project_root, 'source_documents')
    source_docs = read_source_files(source_folder)
    
    if not source_docs:
        logger.warning("No source documents found.")
        return

    for file_name, content in source_docs:
        ingest_source_document(file_name, content)
        logger.info(f"Ingested: {file_name}")

    logger.info("Source document ingestion completed")

if __name__ == "__main__":
    main()
