from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.logger import get_logger
from app.utils.error_handler import handle_exception
from app.config import settings
from .models import Response, ResponseRequest
from openai import OpenAI

async def generate_response(request: ResponseRequest, db: Session = Depends(get_db)):
    logger = get_logger()
    try:
        logger.info(f"Received response request: {request}")
        openai = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = openai.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "user", "content": request.prompt}
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_p=request.top_p,
            frequency_penalty=request.frequency_penalty,
            presence_penalty=request.presence_penalty,
            # ... (Add any other model-specific parameters)
        )
        db_response = Response(
            text=response.choices[0].message.content,
            model=request.model,
            parameters=str(request.parameters),
            generation_time=datetime.utcnow(),
            prompt_id=request.prompt_id
        )
        db.add(db_response)
        db.commit()
        db.refresh(db_response)
        logger.info(f"Generated response: {db_response}")
        return db_response
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API Error: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to OpenAI API")
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return handle_exception(e, logger)