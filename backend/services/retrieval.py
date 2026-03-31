"""
Retrieval service — loads the FAISS index and exposes similarity search.
"""

from __future__ import annotations

import os
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain.schema import Document

from app.core.config import get_settings
from app.core.logging import logger
from app.services.embedding import get_embeddings


_vectorstore: FAISS | None = None


def load_vectorstore() -> FAISS | None:
    """Load the FAISS index from disk.  Returns *None* if the path is missing."""
    global _vectorstore
    if _vectorstore is not None:
        return _vectorstore

    settings = get_settings()
    index_path = Path(settings.FAISS_INDEX_PATH)

    if not index_path.exists():
        logger.warning("FAISS index not found at %s — retrieval disabled", index_path)
        return None

    logger.info("Loading FAISS index from %s", index_path)
    _vectorstore = FAISS.load_local(
        str(index_path),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )
    logger.info("FAISS index loaded (%d vectors)", _vectorstore.index.ntotal)
    return _vectorstore


def is_vectorstore_ready() -> bool:
    return _vectorstore is not None


def retrieve_documents(
    query: str,
    top_k: int | None = None,
    score_threshold: float | None = None,
) -> list[tuple[Document, float]]:
    """
    Run similarity search and return (document, score) pairs.
    Lower score = more similar for L2; we normalise so higher = better.
    """
    settings = get_settings()
    k = top_k or settings.RETRIEVAL_TOP_K
    threshold = score_threshold or settings.SIMILARITY_THRESHOLD

    store = load_vectorstore()
    if store is None:
        logger.warning("Vectorstore not available — returning empty results")
        return []

    results = store.similarity_search_with_score(query, k=k)

    # FAISS returns L2 distance — convert to a 0-1 similarity score
    scored: list[tuple[Document, float]] = []
    for doc, distance in results:
        similarity = 1.0 / (1.0 + distance)
        if similarity >= threshold:
            scored.append((doc, round(similarity, 4)))

    logger.debug(
        "Retrieved %d / %d docs above threshold %.2f for query: %s",
        len(scored),
        len(results),
        threshold,
        query[:80],
    )
    return scored