"""
Ingest raw documents from data/raw/ into chunked, processed documents
ready for FAISS indexing.

Supports: .txt, .md, .csv, .json

Usage:
    cd backend
    python scripts/ingest_docs.py
"""

import os
import sys
import json
import csv
from pathlib import Path
from typing import List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.core.config import get_settings

# ------------------------------------------------------------------ #
#  Config
# ------------------------------------------------------------------ #

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
SAMPLE_FAQ_DIR = Path("data/sample_faqs")


# ------------------------------------------------------------------ #
#  Loaders — one per file type
# ------------------------------------------------------------------ #

def load_txt(path: Path) -> List[Document]:
    text = path.read_text(encoding="utf-8")
    return [Document(page_content=text, metadata={"source": path.name, "type": "txt"})]


def load_md(path: Path) -> List[Document]:
    text = path.read_text(encoding="utf-8")
    return [Document(page_content=text, metadata={"source": path.name, "type": "md"})]


def load_csv_file(path: Path) -> List[Document]:
    """Each row becomes a document. Concatenates all columns into content."""
    docs = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            content = " | ".join(f"{k}: {v}" for k, v in row.items() if v)
            docs.append(
                Document(
                    page_content=content,
                    metadata={"source": path.name, "type": "csv", "row": i},
                )
            )
    return docs


def load_json_file(path: Path) -> List[Document]:
    """
    Expects either:
      - A list of objects with 'question'/'answer' or 'content' fields
      - A single object with a 'faqs' key containing a list
    """
    data = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(data, dict) and "faqs" in data:
        data = data["faqs"]

    if not isinstance(data, list):
        data = [data]

    docs = []
    for i, item in enumerate(data):
        if "question" in item and "answer" in item:
            content = f"Q: {item['question']}\nA: {item['answer']}"
        elif "content" in item:
            content = item["content"]
        else:
            content = json.dumps(item)

        docs.append(
            Document(
                page_content=content,
                metadata={
                    "source": path.name,
                    "type": "json",
                    "index": i,
                    "category": item.get("category", ""),
                },
            )
        )
    return docs


LOADERS = {
    ".txt": load_txt,
    ".md": load_md,
    ".csv": load_csv_file,
    ".json": load_json_file,
}


# ------------------------------------------------------------------ #
#  Chunking
# ------------------------------------------------------------------ #

def chunk_documents(docs: List[Document]) -> List[Document]:
    settings = get_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )
    chunks = splitter.split_documents(docs)
    print(f"  Chunked {len(docs)} documents into {len(chunks)} chunks")
    return chunks


# ------------------------------------------------------------------ #
#  Main
# ------------------------------------------------------------------ #

def ingest_directory(directory: Path) -> List[Document]:
    """Load and chunk all supported files from a directory."""
    if not directory.exists():
        print(f"  Directory not found: {directory} — skipping")
        return []

    all_docs = []
    files = sorted(directory.iterdir())
    supported = [f for f in files if f.suffix in LOADERS and f.is_file()]

    if not supported:
        print(f"  No supported files in {directory}")
        return []

    for filepath in supported:
        loader = LOADERS[filepath.suffix]
        try:
            docs = loader(filepath)
            print(f"  Loaded {filepath.name}: {len(docs)} document(s)")
            all_docs.extend(docs)
        except Exception as e:
            print(f"  ERROR loading {filepath.name}: {e}")

    return all_docs


def save_processed(chunks: List[Document], output_path: Path) -> None:
    """Save processed chunks as JSON for inspection and reuse."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    records = []
    for chunk in chunks:
        records.append({
            "content": chunk.page_content,
            "metadata": chunk.metadata,
        })

    output_path.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"  Saved {len(records)} chunks to {output_path}")


def main():
    print("=" * 60)
    print("  Document Ingestion Pipeline")
    print("=" * 60)

    all_chunks = []

    # Ingest from data/raw/
    print(f"\n[1/2] Loading from {RAW_DIR}/")
    raw_docs = ingest_directory(RAW_DIR)
    if raw_docs:
        raw_chunks = chunk_documents(raw_docs)
        all_chunks.extend(raw_chunks)

    # Ingest from data/sample_faqs/
    print(f"\n[2/2] Loading from {SAMPLE_FAQ_DIR}/")
    faq_docs = ingest_directory(SAMPLE_FAQ_DIR)
    if faq_docs:
        faq_chunks = chunk_documents(faq_docs)
        all_chunks.extend(faq_chunks)

    if not all_chunks:
        print("\nNo documents found. Add files to data/raw/ or data/sample_faqs/")
        print("Supported formats: .txt, .md, .csv, .json")
        return

    # Save processed output
    print(f"\nTotal chunks: {len(all_chunks)}")
    save_processed(all_chunks, PROCESSED_DIR / "chunks.json")

    print("\nDone! Run 'python scripts/build_index.py' to create the FAISS index.")


if __name__ == "__main__":
    main()