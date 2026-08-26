from sqlalchemy.orm import Session
import logging
from app.db.models import Document, DocumentChunk
from app.ingestion.parser import parse_pdf
from app.ingestion.chunker import chunk_pages
from app.ingestion.embeddings import embed_texts
from app.storage.object_storage import ObjectStorage


storage = ObjectStorage()
logger = logging.getLogger(__name__)

def ingest_document(
    document: Document,
    db: Session,
):

    try:

        # download PDF
        pdf_bytes = storage.download(
            document.storage_key
        )

        # parse PDF
        pages = parse_pdf(
            pdf_bytes
        )

        # chunk
        chunks = chunk_pages(
            pages
        )

        # generate embeddings
        embeddings = embed_texts(
            [
                chunk["text"]
                for chunk in chunks
            ]
        )

        # store chunks
        for chunk, embedding in zip(
            chunks,
            embeddings,
        ):

            db_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=chunk["chunk_index"],
                text=chunk["text"],
                page_start=chunk["page_start"],
                page_end=chunk["page_end"],
                embedding=embedding,
            )

            db.add(db_chunk)

        # mark document ready in postgres db
        document.status = "READY"

        db.commit()

    except Exception:
        
        logger.error("Document pipeline failed. ")
        document.status = "FAILED"
        db.commit()

        raise