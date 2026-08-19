"""add hnsw index to document chunks

Revision ID: 684555dca1a2
Revises: 275b0b4628b0
Create Date: 2026-08-18 15:21:39.606078

"""
from alembic import op


revision = "684555dca1a2"
down_revision = "275b0b4628b0"
branch_labels = None
depends_on = None


def upgrade():

    op.execute(
        """
        CREATE INDEX document_chunks_embedding_idx
        ON document_chunks
        USING hnsw (embedding vector_cosine_ops)
        """
    )


def downgrade():

    op.execute(
        """
        DROP INDEX IF EXISTS document_chunks_embedding_idx
        """
    )