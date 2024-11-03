from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from app.utils.logger import get_logger
from openai.error import OpenAIError
from sqlalchemy.exc import OperationalError

async def handle_exception(exc: Exception, logger: get_logger, request: Request) -> JSONResponse:
    """
    Handles exceptions raised during request processing, logs the error, and returns a formatted error response.

    Args:
        exc: The exception object representing the error.
        logger: A logging.Logger instance for logging the error.
        request: The FastAPI request object.

    Returns:
        A JSONResponse containing a formatted error message.
    """
    logger.error(f"Request: {request.method} {request.url}\nError: {exc}")

    if isinstance(exc, OpenAIError):
        error_message = f"OpenAI API Error: {exc}"
        status_code = 500
    elif isinstance(exc, OperationalError):
        error_message = f"Database Error: {exc}"
        status_code = 500
    elif isinstance(exc, HTTPException):
        error_message = exc.detail
        status_code = exc.status_code
    else:
        error_message = "An unexpected error occurred. Please try again later."
        status_code = 500

    return JSONResponse(status_code=status_code, content={"detail": error_message})