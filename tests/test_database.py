import pytest
from app.routers.prompts import models as prompt_models
from app.routers.responses import models as response_models
from app.database import SessionLocal, engine
from app.config import settings
from app.utils.auth import create_access_token
from app.utils.logger import get_logger
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from openai.error import OpenAIError

# Configure test environment
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.replace("postgres://", "postgresql://")

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

def test_prompt_model_creation(db_session):
    prompt = prompt_models.Prompt(text="My test prompt", model="text-davinci-003")
    db_session.add(prompt)
    db_session.commit()
    assert prompt.id is not None

def test_response_model_creation(db_session):
    response = response_models.Response(
        text="This is a mocked response",
        model="text-davinci-003",
        generation_time=datetime.utcnow(),
    )
    db_session.add(response)
    db_session.commit()
    assert response.id is not None

def test_create_prompt_success(client, db_session):
    prompt_data = {"text": "My test prompt", "model": "text-davinci-003"}
    response = client.post("/prompts", json=prompt_data)
    assert response.status_code == 200
    assert response.json()["text"] == prompt_data["text"]

def test_create_prompt_failure(client, db_session):
    prompt_data = {"text": "", "model": "text-davinci-003"}
    response = client.post("/prompts", json=prompt_data)
    assert response.status_code == 422

def test_create_response_success(client, db_session, mock_openai):
    prompt = prompt_models.Prompt(text="My test prompt", model="text-davinci-003")
    db_session.add(prompt)
    db_session.commit()
    response_data = {
        "prompt": "My test prompt",
        "model": "text-davinci-003",
        "prompt_id": prompt.id,
    }
    response = client.post("/responses", json=response_data)
    assert response.status_code == 200
    assert response.json()["text"] == "This is a mocked response"

def test_create_response_failure(client, db_session, mock_openai):
    response_data = {"prompt": "My test prompt", "model": "invalid_model"}
    response = client.post("/responses", json=response_data)
    assert response.status_code == 422

def test_generate_response_success(db_session, mock_openai):
    prompt = prompt_models.Prompt(text="My test prompt", model="text-davinci-003")
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
    prompt = prompt_models.Prompt(text="My test prompt", model="text-davinci-003")
    db_session.add(prompt)
    db_session.commit()
    response_data = {
        "prompt": "My test prompt",
        "model": "text-davinci-003",
        "prompt_id": prompt.id,
    }
    response = client.post("/responses", json=response_data)
    assert response.status_code == 500

def test_create_access_token():
    token = create_access_token(1)
    assert token is not None

def test_verify_token():
    token = create_access_token(1)
    payload = verify_token(token)
    assert payload["sub"] == 1

def test_authenticate_user(db_session, mock_request):
    user = authenticate_user(mock_request, db_session)
    assert user.id == 1

def test_handle_openai_error():
    with patch("app.utils.error_handler.OpenAIError") as mock_error:
        mock_error.return_value.args = ("Mocked OpenAI Error",)
        response = handle_exception(mock_error, get_logger(), MagicMock())
        assert response.status_code == 500
        assert response.json()["detail"] == "OpenAI API Error: Mocked OpenAI Error"

def test_handle_database_error():
    with patch("app.utils.error_handler.OperationalError") as mock_error:
        mock_error.return_value.args = ("Mocked Database Error",)
        response = handle_exception(mock_error, get_logger(), MagicMock())
        assert response.status_code == 500
        assert response.json()["detail"] == "Database Error: Mocked Database Error"

def test_handle_http_exception():
    mock_http_exception = HTTPException(status_code=400, detail="Bad Request")
    response = handle_exception(
        mock_http_exception, get_logger(), MagicMock()
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Bad Request"

def test_handle_unexpected_error():
    mock_error = Exception("Mocked Unexpected Error")
    response = handle_exception(mock_error, get_logger(), MagicMock())
    assert response.status_code == 500
    assert response.json()["detail"] == "An unexpected error occurred. Please try again later."

def test_validate_prompt_valid_input():
    prompt_data = {"text": "My test prompt", "model": "text-davinci-003"}
    validated_prompt = validate_prompt(prompt_data)
    assert validated_prompt["text"] == "My test prompt"
    assert validated_prompt["model"] == "text-davinci-003"

def test_validate_prompt_invalid_input():
    prompt_data = {"text": "", "model": "text-davinci-003"}
    with pytest.raises(Exception):
        validate_prompt(prompt_data)

def test_validate_response_valid_input():
    response_data = {"prompt": "My test prompt", "model": "text-davinci-003"}
    validated_response = validate_response(response_data)
    assert validated_response["prompt"] == "My test prompt"
    assert validated_response["model"] == "text-davinci-003"

def test_validate_response_invalid_input():
    response_data = {"prompt": "My test prompt", "model": "invalid_model"}
    with pytest.raises(Exception):
        validate_response(response_data)