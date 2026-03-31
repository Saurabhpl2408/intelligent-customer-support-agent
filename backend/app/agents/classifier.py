"""
Intent classification agent — uses the LLM to map a customer message to one
of the predefined intent categories.
"""

from __future__ import annotations

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

from app.core.config import get_settings
from app.core.constants import INTENT_CATEGORIES, CLASSIFIER_PROMPT
from app.core.logging import logger


def classify_intent(message: str) -> str:
    """
    Send the customer message through a lightweight LLM call that returns
    a single intent label.  Falls back to ``"general_faq"`` on failure.
    """
    settings = get_settings()

    llm = ChatOpenAI(
        model=settings.OPENAI_CHAT_MODEL,
        temperature=0.0,
        max_tokens=30,
        openai_api_key=settings.OPENAI_API_KEY,
    )

    prompt = CLASSIFIER_PROMPT.format(
        intents=", ".join(INTENT_CATEGORIES),
        message=message,
    )

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        label = response.content.strip().lower().replace('"', "").replace("'", "")

        if label in INTENT_CATEGORIES:
            logger.debug("Classified intent: %s", label)
            return label

        logger.warning(
            "LLM returned unknown intent '%s' — falling back to general_faq", label
        )
        return "general_faq"

    except Exception as exc:
        logger.error("Intent classification failed: %s", exc)
        return "general_faq"