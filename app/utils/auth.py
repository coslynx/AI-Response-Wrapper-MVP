from typing import Optional
from datetime import timedelta, datetime
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from app.database import get_db
from sqlalchemy.orm import Session
from app.database.models import User
from app.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user_id, "exp": datetime.utcnow() + expires_delta}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, issuer: str = None, audience: str = None):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def authenticate_user(request: Request, db: Session = Depends(get_db)):
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=401, detail="Authorization header is missing"
        )
    token = authorization.split(" ")[1]
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

bearer_scheme = HTTPBearer()

def get_current_user(request: Request, db: Session = Depends(get_db)):
    user = authenticate_user(request, db)
    return user