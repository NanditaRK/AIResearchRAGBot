# AI Research RAG Bot

A RAG bot to help me with the questions I have when reading research papers on AI. Made it simple because the main goal of this was functionality.

=)

# Setup/Installation

Clone the repository
```bash
git clone https://github.com/NanditaRK/AIResearchRAGBot.git
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

Add the documents you want to be stored and index in `data/documents/`

Index your documents
```bash
uv run python build_index.py
```

Run RAG server
```bash
uv run uvicorn app.main:app --reload
```

Send a request at `/ask` endpoint.
