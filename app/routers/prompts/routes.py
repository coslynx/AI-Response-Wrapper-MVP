from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.utils.logger import get_logger
from .models import Prompt, PromptCreate

router = APIRouter(
    prefix="/prompts",
    tags=["prompts"],
    responses={404: {"description": "Prompt not found"}},
)

@router.post("/", response_model=Prompt)
async def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    logger = get_logger()
    try:
        db_prompt = Prompt(**prompt.dict())
        db.add(db_prompt)
        db.commit()
        db.refresh(db_prompt)
        logger.info(f"Created new prompt: {db_prompt.id}")
        return db_prompt
    except Exception as e:
        logger.error(f"Error creating prompt: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")