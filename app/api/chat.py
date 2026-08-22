from fastapi import APIRouter, Depends, Form
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth import get_current_active_user
from app.db.database import get_db
from app.db.models import Document
from app.llm.gemini import generate_answer
from app.retrieval.search import search_similar_chunks


router = APIRouter()


@router.post("/ask")
async def ask(
    question: str = Form(...),
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    chunks = search_similar_chunks(
        question=question,
        user_id=current_user["user"].email,
        db=db,
        top_k=5,
    )

    answer = generate_answer(
        question=question,
        chunks=chunks,
    )

    document_ids = {chunk.document_id for chunk in chunks}

    documents = db.scalars(
        select(Document).where(
            Document.id.in_(document_ids)
        )
    ).all()

    documents_by_id = {
        document.id: document
        for document in documents
    }

    sources = []

    for chunk in chunks:
        document = documents_by_id.get(chunk.document_id)

        sources.append({
            
            "document": document.filename if document else None,
            "page_start": chunk.page_start,
            "page_end": chunk.page_end,
        })

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }