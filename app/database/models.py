from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base  # Importing the Base class from our database module

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    api_key = Column(String, nullable=False)

class Prompt(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    model = Column(String, nullable=False)
    parameters = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="prompts")
    responses = relationship("Response", back_populates="prompt")

class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    model = Column(String, nullable=False)
    parameters = Column(String)
    generation_time = Column(DateTime, nullable=False)
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    prompt = relationship("Prompt", back_populates="responses")