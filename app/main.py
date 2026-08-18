from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from .embeddings import EmbeddingModel
from .vector_store import VectorStore
from .rag import RAG


app = FastAPI(
    title="Customer Support RAG",
)


INDEX_DIR = "index"


class Question(BaseModel):

    question: str

    top_k: int = 5


embedding_model = EmbeddingModel()


vector_store = VectorStore.load(
    INDEX_DIR
)


rag = RAG(
    vector_store=vector_store,
    embedding_model=embedding_model,
)


@app.get("/health")
def health():

    return {
        "status": "ok",
        "documents": len(
            vector_store.chunks
        ),
    }


@app.post("/ask")
def ask(request: Question):

    return rag.answer(
        question=request.question,
        top_k=request.top_k,
    )