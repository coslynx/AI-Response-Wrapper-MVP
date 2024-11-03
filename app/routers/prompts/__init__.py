from fastapi import APIRouter, Depends
from .models import Prompt, PromptCreate
from app.database import get_db
from app.utils.logger import get_logger  # For logging
from sqlalchemy.orm import Session
from fastapi import HTTPException

router = APIRouter(
    prefix="/prompts",
    tags=["prompts"],
    responses={404: {"description": "Prompt not found"}},
)

@router.post("/", response_model=Prompt)
async def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    logger = get_logger()  # Get the logger instance
    try:
        db_prompt = Prompt(**prompt.dict())  # Create a Prompt object from the validated data
        db.add(db_prompt)  # Add the prompt to the database session
        db.commit()  # Commit changes to the database
        db.refresh(db_prompt)  # Update the object with database-generated ID
        logger.info(f"Created new prompt: {db_prompt.id}")  # Log success
        return db_prompt  # Return the created prompt
    except Exception as e:  # Handle database errors or unexpected issues
        logger.error(f"Error creating prompt: {e}")  # Log the error
        raise HTTPException(status_code=500, detail="Internal server error")