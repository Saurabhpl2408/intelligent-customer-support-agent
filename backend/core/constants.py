"""
Application-wide constants: intent categories, prompt templates, and defaults.
"""



INTENT_CATEGORIES: list[str] = [
    "billing_inquiry",
    "refund_request",
    "order_status",
    "shipping_info",
    "product_info",
    "account_management",
    "technical_support",
    "password_reset",
    "cancellation",
    "complaint",
    "feedback",
    "return_policy",
    "warranty",
    "payment_methods",
    "subscription_management",
    "promo_code",
    "contact_human_agent",
    "general_faq",
    "greeting",
    "goodbye",
    "out_of_scope",
]


SYSTEM_PROMPT = """You are a friendly, professional customer-support assistant \
for an e-commerce company.  Your role is to help customers with their questions \
by using the knowledge base provided to you through retrieval context.

Guidelines:
1. Always ground your answers in the retrieved context.  If the context does not \
   contain enough information, say so honestly and offer to connect the customer \
   with a human agent.
2. Keep responses concise (2-4 sentences) unless the customer asks for detail.
3. Never fabricate order numbers, prices, or policy details.
4. If the customer is upset, acknowledge their frustration before answering.
5. When the intent is "contact_human_agent", confirm that you will escalate.
"""

CLASSIFIER_PROMPT = """Classify the following customer message into exactly one \
intent from this list: {intents}.

Message: "{message}"

Respond with ONLY the intent label, nothing else."""

RAG_CONTEXT_PROMPT = """Use the following retrieved context to answer the \
customer's question.  If the context is insufficient, say you don't have enough \
information and offer to escalate.

--- Retrieved Context ---
{context}
--- End Context ---

Customer question: {question}"""


DEFAULT_FALLBACK_REPLY = (
    "I'm sorry, I wasn't able to find an answer to that.  "
    "Would you like me to connect you with a human support agent?"
)

ESCALATION_REPLY = (
    "I understand you'd like to speak with a human agent.  "
    "Let me transfer you now — a support representative will be with you shortly."
)