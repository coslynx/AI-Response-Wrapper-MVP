import logging
from app.config import settings

def get_logger(level: str = settings.LOG_LEVEL) -> logging.Logger:
    """
    Returns a configured logger instance.

    Args:
        level: The logging level to use (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"). Defaults to `settings.LOG_LEVEL`.

    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger("ai_response_wrapper")
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename="app.log",
        filemode="a",
    )
    return logger