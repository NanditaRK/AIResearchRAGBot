#!/bin/sh
set -e

echo "Waiting for database and running migrations..."

until uv run --no-dev alembic upgrade head; do
    echo "Database not ready yet. Retrying in 3 seconds..."
    sleep 3
done

echo "Database migrations complete."
echo "Starting Research RAG API..."

exec uv run --no-dev uvicorn app.main:app --host 0.0.0.0 --port 8000