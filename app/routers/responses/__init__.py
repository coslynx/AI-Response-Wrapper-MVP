from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.utils.logger import get_logger
from app.utils.error_handler import handle_exception
from .models import Response
from .services import generate_response
from .routes import router as responses_router

router = APIRouter(
    prefix="/responses",
    tags=["responses"],
    responses={404: {"description": "Response not found"}},
)

# Include the router defined in routes.py
router.include_router(responses_router)

# Example: Middleware for logging API calls
@router.middleware("http")
async def log_api_call(request: Request, call_next):
    logger = get_logger()
    logger.info(f"API Call: {request.method} {request.url}")
    response = await call_next(request)
    return response