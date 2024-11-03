from typing import Union, Dict, Any
from pydantic import BaseModel, validator, ValidationError
from app.utils.logger import get_logger
from app.config import settings  # For accessing configuration settings

class DataValidator:

    def __init__(self):
        self.logger = get_logger()

    def validate_prompt(self, prompt: Dict[str, Any]) -> Dict[str, Any]:
        """Validates a prompt input.

        Args:
            prompt (Dict[str, Any]): The prompt dictionary.

        Returns:
            Dict[str, Any]: The validated prompt dictionary.

        Raises:
            ValidationError: If the prompt is invalid.
        """
        try:
            prompt_model = PromptCreate(**prompt)
            return prompt_model.dict()
        except ValidationError as e:
            self.logger.error(f"Prompt validation error: {e}")
            raise

    def validate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Validates a response input.

        Args:
            response (Dict[str, Any]): The response dictionary.

        Returns:
            Dict[str, Any]: The validated response dictionary.

        Raises:
            ValidationError: If the response is invalid.
        """
        try:
            response_model = ResponseRequest(**response)
            return response_model.dict()
        except ValidationError as e:
            self.logger.error(f"Response validation error: {e}")
            raise

class PromptCreate(BaseModel):
    text: str
    model: str = "text-davinci-003"  # Example model name
    max_tokens: int = 100  # Example maximum tokens
    temperature: float = 0.5  # Example temperature
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

    @validator("max_tokens")
    def max_tokens_positive(cls, value):
        if value <= 0:
            raise ValueError("max_tokens must be a positive integer")
        return value

    @validator("temperature")
    def temperature_range(cls, value):
        if value < 0 or value > 1:
            raise ValueError("temperature must be between 0 and 1")
        return value

    @validator("top_p")
    def top_p_range(cls, value):
        if value < 0 or value > 1:
            raise ValueError("top_p must be between 0 and 1")
        return value

    @validator("frequency_penalty")
    def frequency_penalty_range(cls, value):
        if value < 0 or value > 1:
            raise ValueError("frequency_penalty must be between 0 and 1")
        return value

    @validator("presence_penalty")
    def presence_penalty_range(cls, value):
        if value < 0 or value > 1:
            raise ValueError("presence_penalty must be between 0 and 1")
        return value

class ResponseRequest(BaseModel):
    prompt: str
    model: str
    parameters: Union[Dict[str, Any], None] = None
    # ... (Other parameters based on the OpenAI model)

    @validator("model")
    def model_validation(cls, value):
        if value not in settings.VALID_OPENAI_MODELS:
            raise ValueError(f"Invalid OpenAI model: {value}")
        return value