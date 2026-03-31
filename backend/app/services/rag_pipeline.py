"""
RAG pipeline — retrieves relevant documents and builds the augmented context
that is injected into the agent's prompt.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

from app.core.logging import logger
from app.models.schemas import SourceDocument
from app.services.retrieval import retrieve_documents


@dataclass
class RAGResult:
    context: str
    sources: List[SourceDocument]


def run_rag_pipeline(query: str, top_k: Optional[int] = None) -> RAGResult:
    """
    1. Embed the query
    2. Retrieve top-k similar documents from FAISS
    3. Format the context block and source metadata
    """
    results = retrieve_documents(query, top_k=top_k)

    if not results:
        logger.info("RAG pipeline returned no relevant documents for: %s", query[:80])
        return RAGResult(context="", sources=[])

    context_parts: List[str] = []
    sources: List[SourceDocument] = []

    for idx, (doc, score) in enumerate(results, 1):
        context_parts.append(f"[{idx}] {doc.page_content}")
        sources.append(
            SourceDocument(
                content=doc.page_content,
                source=doc.metadata.get("source"),
                score=score,
            )
        )

    context = "\n\n".join(context_parts)
    logger.info("RAG pipeline built context from %d documents", len(sources))
    return RAGResult(context=context, sources=sources)