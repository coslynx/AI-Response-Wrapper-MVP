import pytest
from app.utils.auth import create_access_token, verify_token
from app.utils.error_handler import handle_exception
from app.utils.logger import get_logger
from app.utils.data_validation import validate_prompt, validate_response
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from datetime import datetime
from openai.error import OpenAIError
from app.config import settings

def test_create_access_token_valid_user():
    user_id = 1
    token = create_access_token(user_id)
    assert token is not None

def test_create_access_token_expires_delta():
    user_id = 1
    expires_delta = datetime.timedelta(minutes=15)
    token = create_access_token(user_id, expires_delta)
    assert token is not None

def test_verify_token_valid_token():
    user_id = 1
    token = create_access_token(user_id)
    payload = verify_token(token)
    assert payload["sub"] == user_id

def test_verify_token_invalid_token():
    token = "invalid_token"
    with pytest.raises(Exception):
        verify_token(token)

def test_handle_openai_error_generic():
    mock_error = OpenAIError("Mocked OpenAI Error")
    mock_request = MagicMock()
    response = handle_exception(mock_error, get_logger(), mock_request)
    assert response.status_code == 500
    assert response.json()["detail"] == "OpenAI API Error: Mocked OpenAI Error"

def test_handle_openai_error_specific_code():
    mock_error = OpenAIError("Mocked OpenAI Error", status=400)
    mock_request = MagicMock()
    response = handle_exception(mock_error, get_logger(), mock_request)
    assert response.status_code == 400
    assert response.json()["detail"] == "OpenAI API Error: Mocked OpenAI Error"

def test_handle_database_error():
    mock_error = Exception("Mocked Database Error")
    mock_request = MagicMock()
    response = handle_exception(mock_error, get_logger(), mock_request)
    assert response.status_code == 500
    assert response.json()["detail"] == "Database Error: Mocked Database Error"

def test_handle_http_exception_valid():
    mock_http_exception = HTTPException(status_code=400, detail="Bad Request")
    mock_request = MagicMock()
    response = handle_exception(mock_http_exception, get_logger(), mock_request)
    assert response.status_code == 400
    assert response.json()["detail"] == "Bad Request"

def test_handle_unexpected_error():
    mock_error = Exception("Mocked Unexpected Error")
    mock_request = MagicMock()
    response = handle_exception(mock_error, get_logger(), mock_request)
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