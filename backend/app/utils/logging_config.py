import logging
import os

def setup_logging():
    log_file = os.getenv('LOG_FILE', 'E:/Github/swarm-openai/app.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Create a logger instance
logger = setup_logging()
