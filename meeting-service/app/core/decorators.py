"""
App decorators.
"""

from functools import wraps
import time

from loguru import logger


def log_execution_time(func):
    """Decorator to log the execution time of a function."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        logger.info(f"{func.__name__} executed in {elapsed_time:.2f} seconds")
        return result

    return wrapper
