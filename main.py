from logger import get_logger

# Get the logger instance
logger = get_logger()

def some_function():
    logger.info('This is an info message')
    logger.error('This is an error message')

# Example usage
if __name__ == "__main__":
    some_function()
