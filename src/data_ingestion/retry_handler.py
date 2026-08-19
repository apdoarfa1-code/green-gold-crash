import asyncio
from functools import wraps
from typing import Callable, Any
from config.logging_config import logger
from src.core.exceptions import IngestionError


def retry_on_exception(max_attempts: int = 3, delay: float = 2.0, backoff: float = 2.0):
    """Decorator providing robust retry logic with exponential backoff."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay
            while attempt < max_attempts:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed in {func.__name__}: {str(e)}. Retrying in {current_delay}s..."
                    )
                    if attempt >= max_attempts:
                        logger.error(f"Max retry attempts ({max_attempts}) reached for {func.__name__}.")
                        raise IngestionError(f"Operation failed after {max_attempts} attempts: {str(e)}") from e
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator
