from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import DocumentChunk
from app.ingestion.embeddings import embed_texts


def search_similar_chunks(
    question: str,
    db: Session,
    top_k: int = 5,
) -> list[DocumentChunk]:

    # Embed the user's question
    question_embedding = embed_texts(
        [question]
    )[0]

    # pgvector cosine distance
    statement = (
        select(DocumentChunk)
        .order_by(
            DocumentChunk.embedding.cosine_distance(
                question_embedding
            )
        )
        .limit(top_k)
    )

    results = db.execute(statement).scalars().all()

    return results