import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_message(message: str):
    logger.info(message)