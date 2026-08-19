"""enable pgvector and create document chunks

Revision ID: 275b0b4628b0
Revises: 831fcea3b59b
Create Date: 2026-08-18 15:00:49.242944

"""
revision = "275b0b4628b0"
down_revision = "831fcea3b59b"
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


def upgrade():

    op.execute(
        "CREATE EXTENSION IF NOT EXISTS vector"
    )

    op.create_table(
        "document_chunks",

        sa.Column(
            "id",
            sa.UUID(),
            primary_key=True,
        ),

        sa.Column(
            "document_id",
            sa.UUID(),
            sa.ForeignKey("documents.id"),
            nullable=False,
        ),

        sa.Column(
            "chunk_index",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "text",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "page_start",
            sa.Integer(),
        ),

        sa.Column(
            "page_end",
            sa.Integer(),
        ),

        sa.Column(
            "embedding",
            Vector(384),
            nullable=False,
        ),
    )


def downgrade():

    op.drop_table("document_chunks")

    op.execute(
        "DROP EXTENSION IF EXISTS vector"
    )