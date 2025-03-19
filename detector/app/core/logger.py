import logging
import sys

def setup_logger(name: str):
    """
    Sets up a logger with the specified name. The logger will output log messages
    to both the console and a file named 'backend_app.log'. The log messages will
    include the timestamp, logger name, log level, and the message.
    Args:
        name (str): The name of the logger.
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) 
    
    # Format log
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # File Handler
    file_handler = logging.FileHandler("detector_app.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Add handlers if not already added
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger
