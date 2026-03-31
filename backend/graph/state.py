"""
Typed state that flows through the LangGraph workflow.
"""

from __future__ import annotations

from typing import TypedDict

from app.models.schemas import ChatMessage, SourceDocument, ConversationStatus


class AgentState(TypedDict):
    """Mutable state passed between graph nodes."""

    # Input
    session_id: str
    message: str
    history: list[ChatMessage]

    # Intermediate
    intent: str
    rag_context: str
    sources: list[SourceDocument]

    # Output
    reply: str
    status: ConversationStatus