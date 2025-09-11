import traceback
import logging

# logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def traceback_handler(e: Exception, env: str):
    """
    Handles exception logging based on environment.
    
    In 'dev', 'sit', and 'uat' environments -> full traceback is printed.
    In all other environments -> only error message is logged (to avoid data leakage).
    
    Args:
        e (Exception): The exception object raised.
        env (str): Current environment (e.g., 'dev', 'sit', 'uat', 'prod').
    
    Example:
        try:
            1 / 0
        except Exception as ex:
            traceback_handler(ex, env="dev")
    """
    allowed_envs = {"dev", "sit", "uat"}
    
    if env.lower() in allowed_envs:
        logger.error("Traceback (most recent call last):")
        traceback.print_exc()
    else:
        logger.error("Exception occurred: %s", str(e))




import traceback
import logging

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def traceback_handler(e: Exception, env: str):
    """
    Handles exception logging based on environment.
    
    In 'dev', 'sit', and 'uat' environments -> full traceback is logged.
    In all other environments -> only error message is logged (to avoid sensitive info leakage).
    
    Args:
        e (Exception): The exception object raised.
        env (str): Current environment (e.g., 'dev', 'sit', 'uat', 'prod').
    
    Example:
        try:
            1 / 0
        except Exception as ex:
            traceback_handler(ex, env="dev")
    """
    allowed_envs = {"dev", "sit", "uat"}
    
    if env.lower() in allowed_envs:
        logger.error("Traceback:\n%s", traceback.format_exc())
    else:
        logger.error("Exception occurred: %s", str(e))


# ---------------- Example Usage ----------------
if __name__ == "__main__":
    # Dev environment → full traceback
    try:
        10 / 0
    except Exception as ex:
        traceback_handler(ex, env="dev")

    # Prod environment → only short error message
    try:
        arr = [1, 2, 3]
        print(arr[5])
    except Exception as ex:
        traceback_handler(ex, env="prod")
