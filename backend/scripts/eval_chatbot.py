"""
Evaluate the chatbot across intent classification accuracy, retrieval
relevance, and end-to-end response quality.

Usage:
    cd backend
    python scripts/eval_chatbot.py                # run all evaluations
    python scripts/eval_chatbot.py --intents      # intent classification only
    python scripts/eval_chatbot.py --retrieval    # retrieval relevance only
    python scripts/eval_chatbot.py --e2e          # end-to-end only
"""

import os
import sys
import json
import time
import argparse
from typing import List, Dict
from dataclasses import dataclass, asdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app.agents.classifier import classify_intent
from app.services.retrieval import retrieve_documents, load_vectorstore
from app.agents.response_generator import generate_response
from app.services.rag_pipeline import run_rag_pipeline


# ------------------------------------------------------------------ #
#  Test Cases
# ------------------------------------------------------------------ #

INTENT_TEST_CASES = [
    {"message": "How do I get a refund?", "expected": "refund_request"},
    {"message": "Where is my order?", "expected": "order_status"},
    {"message": "I want to return this item", "expected": "return_policy"},
    {"message": "What shipping options do you have?", "expected": "shipping_info"},
    {"message": "How do I reset my password?", "expected": "password_reset"},
    {"message": "I want to cancel my subscription", "expected": "cancellation"},
    {"message": "What payment methods do you accept?", "expected": "payment_methods"},
    {"message": "I have a promo code", "expected": "promo_code"},
    {"message": "Tell me about the warranty", "expected": "warranty"},
    {"message": "I need to talk to a real person", "expected": "contact_human_agent"},
    {"message": "Hello!", "expected": "greeting"},
    {"message": "Goodbye, thanks for the help", "expected": "goodbye"},
    {"message": "I want to change my email address", "expected": "account_management"},
    {"message": "This product is terrible, I am very unhappy", "expected": "complaint"},
    {"message": "What can you tell me about your laptop?", "expected": "product_info"},
    {"message": "I want to upgrade my plan", "expected": "subscription_management"},
    {"message": "How much does express shipping cost?", "expected": "shipping_info"},
    {"message": "Can I get a replacement for a defective item?", "expected": "return_policy"},
    {"message": "Your service has been great, keep it up", "expected": "feedback"},
    {"message": "What is the meaning of life?", "expected": "out_of_scope"},
]

RETRIEVAL_TEST_CASES = [
    {
        "query": "How do I get a refund?",
        "expected_source": "refund_policy.md",
    },
    {
        "query": "What are the shipping costs?",
        "expected_source": "shipping_faq.md",
    },
    {
        "query": "I forgot my password",
        "expected_source": "account_faq.md",
    },
    {
        "query": "What is your return policy?",
        "expected_source": "return_policy.md",
    },
    {
        "query": "Do you accept PayPal?",
        "expected_source": "payment_faq.md",
    },
    {
        "query": "How do I track my package?",
        "expected_source": "order_tracking_faq.md",
    },
    {
        "query": "How much is the Pro plan?",
        "expected_source": "subscription_faq.md",
    },
    {
        "query": "Does this come with a warranty?",
        "expected_source": "warranty_faq.md",
    },
]

E2E_TEST_CASES = [
    {
        "message": "How do I get a refund?",
        "must_contain": ["refund", "order"],
        "must_not_contain": ["I don't know"],
    },
    {
        "message": "What shipping options are available?",
        "must_contain": ["shipping", "free"],
        "must_not_contain": ["I don't know"],
    },
    {
        "message": "I want to speak to a human",
        "must_contain": ["human", "agent", "transfer", "representative"],
        "must_not_contain": [],
    },
    {
        "message": "Hello there!",
        "must_contain": ["hello", "hi", "help", "welcome", "hey"],
        "must_not_contain": ["refund", "shipping"],
    },
]


# ------------------------------------------------------------------ #
#  Result tracking
# ------------------------------------------------------------------ #

@dataclass
class TestResult:
    test_name: str
    passed: bool
    expected: str
    actual: str
    details: str = ""
    latency_ms: float = 0.0


# ------------------------------------------------------------------ #
#  Evaluators
# ------------------------------------------------------------------ #

def eval_intent_classification() -> List[TestResult]:
    """Test intent classification accuracy."""
    print("\n" + "=" * 60)
    print("  Intent Classification Evaluation")
    print("=" * 60)

    results = []
    for tc in INTENT_TEST_CASES:
        start = time.time()
        predicted = classify_intent(tc["message"])
        latency = (time.time() - start) * 1000

        passed = predicted == tc["expected"]
        result = TestResult(
            test_name=f"intent: {tc['message'][:50]}",
            passed=passed,
            expected=tc["expected"],
            actual=predicted,
            latency_ms=round(latency, 1),
        )
        results.append(result)

        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] '{tc['message'][:40]}...' -> {predicted} (expected: {tc['expected']}) [{latency:.0f}ms]")

    return results


def eval_retrieval_relevance() -> List[TestResult]:
    """Test that the top retrieved document matches the expected source."""
    print("\n" + "=" * 60)
    print("  Retrieval Relevance Evaluation")
    print("=" * 60)

    load_vectorstore()
    results = []

    for tc in RETRIEVAL_TEST_CASES:
        start = time.time()
        docs = retrieve_documents(tc["query"], top_k=3, score_threshold=0.0)
        latency = (time.time() - start) * 1000

        if not docs:
            result = TestResult(
                test_name=f"retrieval: {tc['query'][:50]}",
                passed=False,
                expected=tc["expected_source"],
                actual="NO RESULTS",
                latency_ms=round(latency, 1),
            )
        else:
            top_source = docs[0][0].metadata.get("source", "unknown")
            top_score = docs[0][1]
            passed = top_source == tc["expected_source"]

            all_sources = [d[0].metadata.get("source", "?") for d, _ in docs] if docs else []
            # Check if expected source is anywhere in top 3
            in_top3 = tc["expected_source"] in [d[0].metadata.get("source", "") for d in [pair[0] for pair in docs]]

            result = TestResult(
                test_name=f"retrieval: {tc['query'][:50]}",
                passed=passed,
                expected=tc["expected_source"],
                actual=top_source,
                details=f"score={top_score:.4f}, in_top3={in_top3}",
                latency_ms=round(latency, 1),
            )

        results.append(result)
        status = "PASS" if result.passed else "FAIL"
        print(f"  [{status}] '{tc['query'][:40]}...' -> {result.actual} (expected: {result.expected}) [{latency:.0f}ms]")

    return results


def eval_e2e_responses() -> List[TestResult]:
    """Test end-to-end response quality."""
    print("\n" + "=" * 60)
    print("  End-to-End Response Evaluation")
    print("=" * 60)

    results = []
    for tc in E2E_TEST_CASES:
        start = time.time()

        # Run the RAG pipeline
        rag_result = run_rag_pipeline(tc["message"])
        reply = generate_response(
            question=tc["message"],
            context=rag_result.context,
            history=None,
        )
        latency = (time.time() - start) * 1000

        reply_lower = reply.lower()

        # Check must_contain (any match counts)
        contains_ok = any(kw.lower() in reply_lower for kw in tc["must_contain"]) if tc["must_contain"] else True

        # Check must_not_contain
        not_contains_ok = all(kw.lower() not in reply_lower for kw in tc["must_not_contain"]) if tc["must_not_contain"] else True

        passed = contains_ok and not_contains_ok

        details_parts = []
        if not contains_ok:
            details_parts.append(f"missing keywords: {tc['must_contain']}")
        if not not_contains_ok:
            found_bad = [kw for kw in tc["must_not_contain"] if kw.lower() in reply_lower]
            details_parts.append(f"unwanted keywords found: {found_bad}")

        result = TestResult(
            test_name=f"e2e: {tc['message'][:50]}",
            passed=passed,
            expected=f"contains={tc['must_contain']}",
            actual=reply[:100],
            details="; ".join(details_parts) if details_parts else "OK",
            latency_ms=round(latency, 1),
        )
        results.append(result)

        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] '{tc['message'][:40]}...' [{latency:.0f}ms]")
        print(f"         Reply: {reply[:120]}...")

    return results


# ------------------------------------------------------------------ #
#  Summary
# ------------------------------------------------------------------ #

def print_summary(all_results: List[TestResult]) -> None:
    print("\n" + "=" * 60)
    print("  EVALUATION SUMMARY")
    print("=" * 60)

    total = len(all_results)
    passed = sum(1 for r in all_results if r.passed)
    failed = total - passed
    avg_latency = sum(r.latency_ms for r in all_results) / total if total else 0

    print(f"\n  Total:    {total}")
    print(f"  Passed:   {passed} ({passed/total*100:.0f}%)" if total else "")
    print(f"  Failed:   {failed}")
    print(f"  Avg Latency: {avg_latency:.0f}ms")

    if failed > 0:
        print(f"\n  Failed tests:")
        for r in all_results:
            if not r.passed:
                print(f"    - {r.test_name}")
                print(f"      Expected: {r.expected}")
                print(f"      Actual:   {r.actual}")
                if r.details:
                    print(f"      Details:  {r.details}")

    # Save results to file
    output_path = Path("data/processed/eval_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps([asdict(r) for r in all_results], indent=2),
        encoding="utf-8",
    )
    print(f"\n  Results saved to {output_path}")


# ------------------------------------------------------------------ #
#  Main
# ------------------------------------------------------------------ #

def main():
    parser = argparse.ArgumentParser(description="Evaluate the chatbot")
    parser.add_argument("--intents", action="store_true", help="Run intent classification eval")
    parser.add_argument("--retrieval", action="store_true", help="Run retrieval relevance eval")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end eval")
    args = parser.parse_args()

    # If no flags, run all
    run_all = not (args.intents or args.retrieval or args.e2e)

    all_results = []

    if run_all or args.intents:
        all_results.extend(eval_intent_classification())

    if run_all or args.retrieval:
        all_results.extend(eval_retrieval_relevance())

    if run_all or args.e2e:
        all_results.extend(eval_e2e_responses())

    print_summary(all_results)


if __name__ == "__main__":
    main()