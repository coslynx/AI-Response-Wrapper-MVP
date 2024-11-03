from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app.utils.logger import get_logger  # For logging
from app.utils.error_handler import handle_exception  # For error handling
from .models import Response
from .services import generate_response

router = APIRouter(
    prefix="/responses",
    tags=["responses"],
    responses={404: {"description": "Response not found"}},
)

@router.post("/", response_model=Response)
async def create_response(request: ResponseRequest, db: Session = Depends(get_db)):
    logger = get_logger()
    try:
        logger.info(f"Received response request: {request}")
        response = await generate_response(request, db)
        logger.info(f"Generated response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return handle_exception(e, logger)