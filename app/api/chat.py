from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.llm.gemini import generate_answer
from app.retrieval.search import search_similar_chunks


router = APIRouter()


@router.post("/ask")
async def ask(
    question: str = Form(...),
    db: Session = Depends(get_db),
):

    # 1. Retrieve relevant chunks
    chunks = search_similar_chunks(
        question=question,
        db=db,
        top_k=5,
    )

    # 2. Generate answer using retrieved context
    answer = generate_answer(
        question=question,
        chunks=chunks,
    )

    # 3. Return answer + sources
    return {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "document_id": str(chunk.document_id),
                "page_start": chunk.page_start,
                "page_end": chunk.page_end,
                "chunk_id": str(chunk.id),
            }
            for chunk in chunks
        ],
    }