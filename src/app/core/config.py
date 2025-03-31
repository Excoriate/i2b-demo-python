from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional # Added Optional just in case, though not strictly needed if all are required

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    All settings here are expected to be provided via environment or .env file.
    """
    COUCHDB_URL: str
    COUCHDB_USER: str
    COUCHDB_PASSWORD: str
    COUCHDB_DB_NAME: str

    APP_HOST: str
    APP_PORT: int
    LOG_LEVEL: str
    PROJECT_NAME: str
    API_V1_STR: str

    # model_config allows loading from a .env file
    # By default, it looks for a file named ".env" in the current working directory
    # or any parent directory.
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

# Instantiate settings - this will raise validation errors if required env vars are missing
settings = Settings()
