"""
Application configuration loaded from environment variables.
"""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Central configuration for the backend service."""

    APP_NAME: str = "Intelligent Customer Support Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    OPENAI_API_KEY: str
    OPENAI_CHAT_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSION: int = 1536

    FAISS_INDEX_PATH: str = "vectorstore/faiss_index"
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64
    RETRIEVAL_TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.72

    MAX_CONVERSATION_TURNS: int = 20
    MAX_TOKENS: int = 1024
    TEMPERATURE: float = 0.2

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()