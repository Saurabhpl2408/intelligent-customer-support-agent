"""
Embedding service — thin wrapper around OpenAI embeddings.
"""

from __future__ import annotations

from langchain_openai import OpenAIEmbeddings

from app.core.config import get_settings
from app.core.logging import logger


_embeddings: OpenAIEmbeddings | None = None


def get_embeddings() -> OpenAIEmbeddings:
    """Return a singleton OpenAIEmbeddings instance."""
    global _embeddings
    if _embeddings is None:
        settings = get_settings()
        logger.info(
            "Initialising OpenAI embeddings (model=%s)", settings.OPENAI_EMBEDDING_MODEL
        )
        _embeddings = OpenAIEmbeddings(
            model=settings.OPENAI_EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
        )
    return _embeddings