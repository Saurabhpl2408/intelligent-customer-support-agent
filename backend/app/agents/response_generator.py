"""
Response generator agent — produces the final customer-facing reply using
RAG context and conversation history.
"""

from __future__ import annotations

from typing import Optional, List

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

from app.core.config import get_settings
from app.core.constants import SYSTEM_PROMPT, RAG_CONTEXT_PROMPT, DEFAULT_FALLBACK_REPLY
from app.core.logging import logger
from app.models.schemas import ChatMessage, MessageRole


def build_langchain_history(history: List[ChatMessage]) -> list:
    """Convert our ChatMessage list into LangChain message objects."""
    messages: list = []
    for msg in history:
        if msg.role == MessageRole.USER:
            messages.append(HumanMessage(content=msg.content))
        elif msg.role == MessageRole.ASSISTANT:
            messages.append(AIMessage(content=msg.content))
    return messages


def generate_response(
    question: str,
    context: str,
    history: Optional[List[ChatMessage]] = None,
) -> str:
    """
    Build the prompt with system instructions + RAG context + chat history,
    then invoke the LLM and return the reply text.
    """
    settings = get_settings()

    llm = ChatOpenAI(
        model=settings.OPENAI_CHAT_MODEL,
        temperature=settings.TEMPERATURE,
        max_tokens=settings.MAX_TOKENS,
        openai_api_key=settings.OPENAI_API_KEY,
    )

    messages: list = [SystemMessage(content=SYSTEM_PROMPT)]

    # Append prior conversation turns
    if history:
        messages.extend(build_langchain_history(history))

    # Build the user turn with injected RAG context
    if context:
        user_content = RAG_CONTEXT_PROMPT.format(context=context, question=question)
    else:
        user_content = question

    messages.append(HumanMessage(content=user_content))

    try:
        response = llm.invoke(messages)
        reply = response.content.strip()
        logger.debug("Generated reply (%d chars)", len(reply))
        return reply

    except Exception as exc:
        logger.error("Response generation failed: %s", exc)
        return DEFAULT_FALLBACK_REPLY