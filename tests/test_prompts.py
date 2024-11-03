import pytest
from app.routers.prompts import models as prompt_models
from app.database import SessionLocal, engine
from app.utils.logger import get_logger
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock

# Configure test environment
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host:port/database_name"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_session():
    Session = TestingSessionLocal
    session = Session()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="session")
def client():
    from app.main import app
    return TestClient(app)

@pytest.fixture(scope="function")
def mock_openai():
    with patch("app.routers.responses.services.OpenAI") as mock_openai:
        mock_openai.return_value.chat.completions.create.return_value = MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(content="This is a mocked response")
                )
            ]
        )
        yield mock_openai

def test_prompt_model_creation(db_session):
    prompt = prompt_models.Prompt(text="My test prompt", model="text-davinci-003")
    db_session.add(prompt)
    db_session.commit()
    assert prompt.id is not None

def test_create_prompt_success(client, db_session):
    prompt_data = {"text": "My test prompt", "model": "text-davinci-003"}
    response = client.post("/prompts", json=prompt_data)
    assert response.status_code == 200
    assert response.json()["text"] == prompt_data["text"]

def test_create_prompt_failure(client, db_session):
    prompt_data = {"text": "", "model": "text-davinci-003"}
    response = client.post("/prompts", json=prompt_data)
    assert response.status_code == 422