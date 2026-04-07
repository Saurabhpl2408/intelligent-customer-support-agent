"""
Build or rebuild the FAISS index from processed document chunks.

Reads from:  data/processed/chunks.json  (output of ingest_docs.py)
Writes to:   vectorstore/faiss_index/

Usage:
    cd backend
    python scripts/build_index.py                  # from processed chunks
    python scripts/build_index.py --from-scratch    # embedded sample FAQs (no files needed)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.core.config import get_settings


CHUNKS_PATH = Path("data/processed/chunks.json")
INDEX_DIR = Path("vectorstore/faiss_index")



SAMPLE_DOCS = [
    Document(
        page_content="Refunds are processed within 5-7 business days after approval. "
        "To request a refund, go to My Orders and click 'Request Refund' on the relevant order.",
        metadata={"source": "refund_policy.md"},
    ),
    Document(
        page_content="We offer free standard shipping on all orders over $50. "
        "Standard shipping takes 5-7 business days. Express shipping (2-3 days) is available for $9.99.",
        metadata={"source": "shipping_faq.md"},
    ),
    Document(
        page_content="To reset your password, click 'Forgot Password' on the login page. "
        "You will receive an email with a reset link valid for 24 hours.",
        metadata={"source": "account_faq.md"},
    ),
    Document(
        page_content="Our return window is 30 days from the delivery date. "
        "Items must be unused and in original packaging. Return shipping is free for defective items.",
        metadata={"source": "return_policy.md"},
    ),
    Document(
        page_content="We accept Visa, Mastercard, American Express, PayPal, and Apple Pay. "
        "All transactions are secured with 256-bit SSL encryption.",
        metadata={"source": "payment_faq.md"},
    ),
    Document(
        page_content="To track your order, go to My Orders and click 'Track' next to your order. "
        "You will also receive tracking updates via email once your order ships.",
        metadata={"source": "order_tracking_faq.md"},
    ),
    Document(
        page_content="Our Pro subscription costs $12.99/month or $99.99/year. "
        "You can cancel anytime from Account Settings > Subscription. "
        "Cancellation takes effect at the end of the current billing cycle.",
        metadata={"source": "subscription_faq.md"},
    ),
    Document(
        page_content="All electronics come with a 1-year manufacturer warranty. "
        "Extended warranty (2 additional years) can be purchased for 15% of the product price.",
        metadata={"source": "warranty_faq.md"},
    ),
    Document(
        page_content="Use promo codes at checkout by entering the code in the 'Discount Code' field. "
        "Only one promo code can be applied per order. Promo codes cannot be combined with other offers.",
        metadata={"source": "promo_faq.md"},
    ),
    Document(
        page_content="Our customer support hours are Monday to Friday, 9 AM to 6 PM EST. "
        "You can reach us via live chat, email at support@example.com, or phone at 1-800-555-0199.",
        metadata={"source": "contact_faq.md"},
    ),
]



def load_from_chunks_json() -> List[Document]:
    """Load processed chunks from the ingestion pipeline output."""
    if not CHUNKS_PATH.exists():
        return []

    data = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))
    docs = []
    for record in data:
        docs.append(
            Document(
                page_content=record["content"],
                metadata=record.get("metadata", {}),
            )
        )
    print(f"Loaded {len(docs)} chunks from {CHUNKS_PATH}")
    return docs



def build_faiss_index(documents: List[Document]) -> FAISS:
    """Embed documents and build a FAISS index."""
    settings = get_settings()

    print(f"Creating embeddings with {settings.OPENAI_EMBEDDING_MODEL}...")
    embeddings = OpenAIEmbeddings(
        model=settings.OPENAI_EMBEDDING_MODEL,
        openai_api_key=settings.OPENAI_API_KEY,
    )

    print(f"Building FAISS index from {len(documents)} documents...")
    store = FAISS.from_documents(documents, embeddings)

    return store


def save_index(store: FAISS) -> None:
    """Save the FAISS index to disk."""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    store.save_local(str(INDEX_DIR))
    print(f"FAISS index saved to {INDEX_DIR}/ ({store.index.ntotal} vectors)")


def main():
    parser = argparse.ArgumentParser(description="Build the FAISS vector index")
    parser.add_argument(
        "--from-scratch",
        action="store_true",
        help="Use built-in sample FAQs instead of processed chunks",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  FAISS Index Builder")
    print("=" * 60)

    if args.from_scratch:
        print("\nUsing built-in sample FAQs...")
        documents = SAMPLE_DOCS
    else:
        documents = load_from_chunks_json()
        if not documents:
            print(f"\nNo chunks found at {CHUNKS_PATH}")
            print("Run 'python scripts/ingest_docs.py' first, or use --from-scratch")
            print("Falling back to built-in sample FAQs...\n")
            documents = SAMPLE_DOCS

    store = build_faiss_index(documents)
    save_index(store)

    print("\n--- Verification ---")
    test_query = "How do I get a refund?"
    results = store.similarity_search_with_score(test_query, k=3)
    print(f"Query: '{test_query}'")
    for i, (doc, score) in enumerate(results, 1):
        source = doc.metadata.get("source", "unknown")
        similarity = 1.0 / (1.0 + score)
        print(f"  [{i}] {source} (similarity: {similarity:.2%}) — {doc.page_content[:80]}...")

    print("\nDone!")


if __name__ == "__main__":
    main()