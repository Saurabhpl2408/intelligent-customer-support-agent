"""
Shared utility helpers.
"""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime


def generate_session_id() -> str:
    """Return a short, URL-safe session identifier."""
    return uuid.uuid4().hex[:16]


def deterministic_id(text: str) -> str:
    """SHA-256 based deterministic ID for deduplication."""
    return hashlib.sha256(text.encode()).hexdigest()[:20]


def utc_now() -> datetime:
    return datetime.utcnow()


def truncate(text: str, max_chars: int = 500) -> str:
    """Truncate text with an ellipsis if it exceeds *max_chars*."""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."


def format_chat_history(history: list[dict]) -> str:
    """Render a list of {role, content} dicts into a readable transcript."""
    lines: list[str] = []
    for msg in history:
        role = msg.get("role", "unknown").capitalize()
        content = msg.get("content", "")
        lines.append(f"{role}: {content}")
    return "\n".join(lines)