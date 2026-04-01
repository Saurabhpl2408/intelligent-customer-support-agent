# Intelligent Customer Support Agent

## What Does This Project Do?

Imagine you're running an online store and hundreds of customers message you every day asking the same kinds of questions — "Where's my order?", "How do I get a refund?", "Do you accept PayPal?". Hiring enough people to answer all of them 24/7 would be expensive.

This project solves that problem. It's an **AI-powered chatbot** that can automatically answer customer questions by reading through your company's FAQ documents, policies, and help articles — and giving accurate, helpful responses in real time.

Think of it like having a super-smart employee who has memorized every page of your company handbook and is available around the clock.

### What Makes It Smart?

Unlike a simple FAQ page where customers have to search for answers themselves, this chatbot:

- **Understands what the customer is asking** — It figures out whether someone wants a refund, needs help tracking an order, or just wants to say hello. It recognizes over 20 different types of customer questions.
- **Finds the right answer from your documents** — Instead of making things up, it searches through your actual company knowledge base to find relevant information before responding. This is called Retrieval-Augmented Generation (RAG).
- **Remembers the conversation** — If a customer asks a follow-up question, the chatbot remembers what was discussed earlier in the same conversation.
- **Knows when to hand off to a human** — If a customer says "I want to talk to a real person," the chatbot recognizes this and initiates a handoff to a human support agent.

### How Does It Work? (The Simple Version)

When a customer sends a message, here's what happens behind the scenes:

```
Customer types: "How do I get a refund?"
        ↓
Step 1: The AI figures out this is a "refund request"
        ↓
Step 2: It searches your knowledge base for refund-related info
        ↓
Step 3: It writes a helpful response using that information
        ↓
Customer sees: "To request a refund, go to My Orders and click
'Request Refund'. Refunds are processed within 5-7 business days."
```

There are three possible paths a message can take:

1. **Normal questions** (most messages) → Search knowledge base → Generate answer
2. **Greetings like "Hello!"** → Skip the search, just respond naturally
3. **"I want to talk to a human"** → Immediately escalate to a human agent

---

## Tech Stack (For Developers)

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS | Chat interface users interact with |
| Backend | FastAPI, Python | API server that processes requests |
| AI Orchestration | LangGraph | Manages the multi-step AI workflow |
| Language Model | GPT-4o-mini (OpenAI) | Understands questions and generates replies |
| Embeddings | text-embedding-3-small (OpenAI) | Converts text into searchable vectors |
| Vector Database | FAISS | Stores and searches document embeddings |
| Deployment | Docker, Azure App Service | Hosts the application in the cloud |

### Architecture

```
User → Next.js Frontend → FastAPI Backend → LangGraph Workflow
                                              ├── Intent Classifier (GPT-4o-mini)
                                              ├── RAG Retrieval (FAISS + OpenAI Embeddings)
                                              └── Response Generator (GPT-4o-mini)
```

### Graph Topology

```
START → classify ──┬── retrieve → respond → END   (most intents)
                   ├── respond → END               (greeting/goodbye)
                   └── escalate → END              (human handoff)
```

---

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── agents/       # Intent classifier + response generator
│   │   ├── core/         # Configuration, constants, logging
│   │   ├── graph/        # LangGraph state machine (state, nodes, workflow)
│   │   ├── models/       # Request/response data schemas
│   │   ├── routes/       # API endpoints (/chat, /health)
│   │   ├── services/     # Embedding, FAISS retrieval, RAG pipeline
│   │   ├── utils/        # Helper functions
│   │   └── main.py       # FastAPI app entry point
│   ├── scripts/          # Doc ingestion, index building, evaluation
│   └── data/             # Raw documents and sample FAQs
│
├── frontend/
│   └── src/
│       ├── app/          # Next.js pages (layout + main chat page)
│       ├── components/   # Chat UI (bubbles, input, typing indicator, etc.)
│       ├── lib/          # API client and TypeScript types
│       └── styles/       # Global CSS and animations
│
└── docker-compose.yml    # Run everything with one command
```

---

## Getting Started

### What You Need

- **Python 3.9+** — The backend is written in Python
- **Node.js 18+** — The frontend uses JavaScript/TypeScript
- **An OpenAI API key** — The AI brain behind the chatbot (costs ~$0.001 per message)

### Step 1: Set Up the Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a file called `.env` in the `backend/` folder:

```
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### Step 2: Build the Knowledge Base

This step reads your FAQ documents and prepares them so the AI can search through them quickly.

```bash
# Load and chunk your documents
python scripts/ingest_docs.py

# Build the searchable index
python scripts/build_index.py
```

Or if you just want to test with sample data:

```bash
python scripts/build_index.py --from-scratch
```

### Step 3: Start the Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

Verify it's running by visiting http://localhost:8000/health in your browser.

### Step 4: Set Up the Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

### Step 5: Use It

Open http://localhost:3000 in your browser. You'll see a chat interface where you can start asking questions.

---

## API Endpoints

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| POST | /api/chat/ | Send a customer message, get an AI response |
| GET | /health | Check if the server is running |

---

## Scripts

| Script | What It Does |
|--------|-------------|
| `scripts/ingest_docs.py` | Reads your documents (.txt, .md, .csv, .json) and splits them into searchable chunks |
| `scripts/build_index.py` | Creates the FAISS vector index from processed chunks |
| `scripts/eval_chatbot.py` | Tests the chatbot's accuracy across intent classification, retrieval, and response quality |

### Running the Evaluation

```bash
python scripts/eval_chatbot.py           # Run all tests
python scripts/eval_chatbot.py --intents # Test intent classification only
```

---

## Adding Your Own Knowledge Base

To make the chatbot answer questions about your business:

1. Add your documents to `backend/data/raw/` (supports .txt, .md, .csv, .json)
2. For FAQ-style content, use JSON format in `backend/data/sample_faqs/`:

```json
{
  "faqs": [
    {
      "question": "What are your store hours?",
      "answer": "We are open Monday to Friday, 9 AM to 6 PM."
    }
  ]
}
```

3. Run the pipeline:

```bash
python scripts/ingest_docs.py
python scripts/build_index.py
```

4. Restart the backend server

---

## Deployment

### Using Docker (Simplest)

```bash
docker-compose up --build
```

This starts both the backend (port 8000) and frontend (port 3000).

### Deploying to Azure

The project is configured for Azure App Service using Docker containers. See the deployment guide for step-by-step instructions on setting up Azure Container Registry and Web Apps through the Azure Portal.

---

## Cost

This project uses OpenAI's most affordable models. A typical conversation turn costs less than $0.001. With $5 of OpenAI credits, you can handle thousands of customer conversations — more than enough for development, testing, and demo purposes.