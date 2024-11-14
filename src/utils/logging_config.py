import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file="bot.log"):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Rotating file handler (keeps the last 5 log files, each up to 1MB)
    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
