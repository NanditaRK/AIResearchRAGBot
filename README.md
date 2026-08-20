# AI Research RAG Bot

A RAG bot to help me reference research papers that I am currently reading to 
answer questions I have. It's pretty simple right now because the project
was made for functionality. Will be adding features as I need it.

**Things to do in the future**
   * make the sources that are listed for user reference document name instead of ids
   * better research paper chunking
   * metadata filtering
   * hybrid BM25 and vector retrieval
   * reranking
   * citation aware generation
   * retrieval evaluation
   * async ingestion

# Setup/Installation

Clone the repository
```bash
git clone https://github.com/NanditaRK/AIResearchRAGBot.git
cd AIResearchRAGBot
```

Create and active a virtual environment
```bash
uv venv
source .venv/bin/activate
```

Install project dependencies into the venv
```bash
uv sync
```

Add environment variables
```bash
cp .env.example .env
```

Run RAG server

1. Run a local server
```bash
uv run uvicorn app.main:app --reload
```
or

2. Use Docker
```bash
docker build -t ragbot .
docker run --env-file .env ragbot
```

Navigate to `/docs` endpoint for API documentation.