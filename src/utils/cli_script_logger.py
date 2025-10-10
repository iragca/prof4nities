from pathlib import Path

from ..config import logger
from functools import wraps


def cli_script_logger(
    LOGGER_DIR: Path = Path("logs"),
    rotation: str = "10 MB",
    level: str = "INFO",
    **logger_kwargs,
) -> callable:
    """
    A decorator to log the execution of a function.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function with logging.
    """

    assert isinstance(LOGGER_DIR, Path), "LOGGER_DIR must be a Path object."

    def decorator(func):
        assert callable(func), "The decorated object must be callable."

        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.add(
                LOGGER_DIR / f"{func.__name__}.log",
                rotation=rotation,
                level=level,
                backtrace=True,
                diagnose=True,
                **logger_kwargs,
            )
            logger.info(f"Executing {func.__name__}({args=}, {kwargs=})")

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}(): {e}")
                raise

            logger.success(f"{func.__name__}() executed successfully.")
            return result

        return wrapper

    return decorator
