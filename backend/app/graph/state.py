"""
Typed state that flows through the LangGraph workflow.
"""

from __future__ import annotations

from typing import TypedDict

from typing import List
from typing import TypedDict

from app.models.schemas import ChatMessage, SourceDocument, ConversationStatus


class AgentState(TypedDict):
    """Mutable state passed between graph nodes."""

    
    session_id: str
    message: str
    history: List[ChatMessage]
    sources: List[SourceDocument]


    intent: str
    rag_context: str

    reply: str
    status: ConversationStatus