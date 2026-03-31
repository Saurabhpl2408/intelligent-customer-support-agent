"""
Pydantic schemas for API request and response payloads.
"""

from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime




class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationStatus(str, Enum):
    ACTIVE = "active"
    ESCALATED = "escalated"
    RESOLVED = "resolved"



class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """Incoming chat turn from the frontend."""
    session_id: str = Field(..., description="Unique conversation session identifier")
    message: str = Field(..., min_length=1, max_length=2000)
    history: List[ChatMessage] = Field(default_factory=list)


class SourceDocument(BaseModel):
    content: str
    source: Optional[str] = None
    score: Optional[float] = None


class ChatResponse(BaseModel):
    """Response returned to the frontend."""
    session_id: str
    reply: str
    intent: Optional[str] = None
    sources: List[SourceDocument] = Field(default_factory=list)
    status: ConversationStatus = ConversationStatus.ACTIVE
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str
    vectorstore_loaded: bool