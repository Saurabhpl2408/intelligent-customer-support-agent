# Intelligent Customer Support Agent

An AI-powered multi-turn chatbot that handles 50+ FAQ intents with context-aware replies, built with **LangGraph**, **FastAPI**, **FAISS**, and **Next.js**.

## Architecture

```
User → NextJS Frontend → FastAPI Backend → LangGraph Workflow
                                             ├── Intent Classifier (GPT-4o-mini)
                                             ├── RAG Retrieval (FAISS + OpenAI Embeddings)
                                             └── Response Generator (GPT-4o-mini)
```

### Graph Topology

```
START → classify ──┬── retrieve → respond → END   (most intents)
                   ├── respond → END               (greeting/goodbye)
                   └── escalate → END              (contact_human_agent)
```

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | Next.js 14, TypeScript, Tailwind CSS |
| Backend   | FastAPI, LangGraph, LangChain       |
| LLM       | GPT-4o-mini (OpenAI)               |
| Embeddings| text-embedding-3-small (OpenAI)    |
| Vector DB | FAISS                              |
| Deployment| Docker, Azure                      |

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- OpenAI API key

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Add your OpenAI API key to .env
# OPENAI_API_KEY=sk-proj-...

# Build the FAISS index
python scripts/build_test_index.py

# Start the server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

### Docker

```bash
docker-compose up --build
```

## API Endpoints

| Method | Endpoint      | Description              |
|--------|---------------|--------------------------|
| POST   | /api/chat/    | Send a chat message      |
| GET    | /health       | Health check + status    |

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── agents/       # Intent classifier, response generator
│   │   ├── core/         # Config, constants, logging
│   │   ├── graph/        # LangGraph state, nodes, workflow
│   │   ├── models/       # Pydantic schemas
│   │   ├── routes/       # FastAPI endpoints
│   │   ├── services/     # Embedding, retrieval, RAG pipeline
│   │   ├── utils/        # Helper functions
│   │   └── main.py       # FastAPI entry point
│   └── scripts/          # Index building, evaluation
│
├── frontend/
│   └── src/
│       ├── app/          # Next.js pages
│       ├── components/   # Chat UI components
│       ├── lib/          # API client, types
│       └── styles/       # Global CSS
│
└── docker-compose.yml
```