import random
import time
import logging
from functools import wraps
from typing import Callable

def random_delay(min_seconds: float, max_seconds: float) -> None:
    """Introduce a random delay to mimic human behavior."""
    try:
        delay = random.uniform(min_seconds, max_seconds)
        logging.debug(f"Applying delay of {delay:.2f} seconds")
        time.sleep(delay)
    except Exception as e:
        logging.error(f"Error in random_delay: {str(e)}")
        raise

def retry(attempts: int = 3, delay: float = 5) -> Callable:
    """Decorator to retry a function on failure."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"Attempt {attempt} failed for {func.__name__}: {str(e)}")
                    if attempt == attempts:
                        logging.error(f"All {attempts} attempts failed for {func.__name__}")
                        raise
                    random_delay(delay, delay + 2)
            return None  # Unreachable, but included for clarity
        return wrapper
    return decorator
