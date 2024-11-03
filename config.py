import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Settings(BaseSettings):
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    DEBUG: bool = os.environ.get("DEBUG", False)
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
    REDIS_HOST: str = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.environ.get("REDIS_PORT", 6379))

    class Config:
        env_file = ".env"  # Load environment variables from .env

settings = Settings()