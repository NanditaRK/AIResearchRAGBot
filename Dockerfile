FROM python:3.13-slim

WORKDIR /app

# system deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# install uv
COPY --from=ghcr.io/astral-sh/uv:0.8.17 /uv /uvx /bin/

# install deps first for docker layer caching
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev


COPY app ./app
COPY migrations ./migrations
COPY alembic.ini ./
COPY templates ./templates
COPY server-startup.sh ./

RUN chmod +x server-startup.sh

EXPOSE 8000

CMD ["/app/server-startup.sh"]