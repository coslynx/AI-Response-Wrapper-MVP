import pytest
from app.routers.responses import models as response_models
from app.database import SessionLocal, engine
from app.utils.logger import get_logger
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock
from app.utils.auth import create_access_token
from datetime import datetime
from openai.error import OpenAIError

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

@pytest.fixture(scope="function")
def mock_request():
    mock_request = MagicMock(
        headers={"Authorization": f"Bearer {create_access_token(1)}"}
    )
    yield mock_request

def test_response_model_creation(db_session):
    response = response_models.Response(
        text="This is a mocked response",
        model="text-davinci-003",
        generation_time=datetime.utcnow(),
    )
    db_session.add(response)
    db_session.commit()
    assert response.id is not None

def test_create_response_success(client, db_session, mock_openai):
    prompt = response_models.Prompt(text="My test prompt", model="text-davinci-003")
    db_session.add(prompt)
    db_session.commit()
    db_session.refresh(prompt)
    response_data = {
        "prompt": "My test prompt",
        "model": "text-davinci-003",
        "prompt_id": prompt.id,
    }
    response = client.post("/responses", json=response_data)
    assert response.status_code == 200
    assert response.json()["text"] == "This is a mocked response"

def test_create_response_failure(client, db_session, mock_openai):
    mock_openai.return_value.chat.completions.create.side_effect = OpenAIError(
        "Mocked OpenAI Error", status=400
    )
    response = client.post(
        "/responses",
        json={"prompt": "My test prompt", "model": "text-davinci-003", "prompt_id": 1},
    )
    assert response.status_code == 500
    assert "Error connecting to OpenAI API" in response.json()["detail"]

def test_generate_response_success(db_session, mock_openai):
    prompt = response_models.Prompt(text="My test prompt", model="text-davinci-003")
    db_session.add(prompt)
    db_session.commit()
    response = response_models.Response(
        text="This is a mocked response",
        model="text-davinci-003",
        generation_time=datetime.utcnow(),
        prompt_id=prompt.id,
    )
    db_session.add(response)
    db_session.commit()
    assert response.id is not None

def test_generate_response_failure(db_session, mock_openai):
    mock_openai.return_value.chat.completions.create.side_effect = Exception(
        "Mocked OpenAI Error"
    )
    prompt = response_models.Prompt(text="My test prompt", model="text-davinci-003")
    db_session.add(prompt)
    db_session.commit()
    response_data = {
        "prompt": "My test prompt",
        "model": "text-davinci-003",
        "prompt_id": prompt.id,
    }
    response = client.post("/responses", json=response_data)
    assert response.status_code == 500