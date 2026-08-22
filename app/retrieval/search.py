from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Document, DocumentChunk
from app.ingestion.embeddings import embed_texts


def search_similar_chunks(
    question: str,
    db: Session,
    user_id: str,
    top_k: int = 5,
) -> list[DocumentChunk]:

    # Embed the user's question
    question_embedding = embed_texts(
        [question]
    )[0]

    # pgvector cosine distance
    statement = (
        select(DocumentChunk)
        .join(Document, DocumentChunk.document_id == Document.id)
        .where(Document.user_id == user_id)
        .order_by(
            DocumentChunk.embedding.cosine_distance(
                question_embedding
            )
        )
        .limit(top_k)
    )

    results = db.execute(statement).scalars().all()

    return results