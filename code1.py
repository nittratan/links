import logging
import logging.config

# Load logging configuration
logging.config.fileConfig('logging.conf')

# Create a logger instance
logger = logging.getLogger('myLogger')

def get_logger():
    """Returns the logger instance."""
    return logger

# -------------------------------------------------

from logger import get_logger

# Get the logger instance
logger = get_logger()

def some_function():
    logger.info('This is an info message')
    logger.error('This is an error message')

# Example usage
if __name__ == "__main__":
    some_function()
