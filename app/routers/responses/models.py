from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    model = Column(String, nullable=False)
    parameters = Column(String)
    generation_time = Column(DateTime, nullable=False)
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    prompt = relationship("Prompt", back_populates="responses")

    def __repr__(self):
        return f"<Response text={self.text[:20]}... model={self.model}>"