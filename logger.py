import logging
import logging.config

# Load logging configuration
logging.config.fileConfig('logging.conf')

# Create a logger instance
logger = logging.getLogger('myLogger')

def get_logger():
    """Returns the logger instance."""
    return logger
