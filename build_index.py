from app.ingestion import ingest_directory
from app.embeddings import EmbeddingModel
from app.vector_store import VectorStore


DOCUMENT_DIRECTORY = "data/documents"
INDEX_DIRECTORY = "index"


print("Loading documents...")

chunks = ingest_directory(
    DOCUMENT_DIRECTORY
)

print(
    f"Total chunks: {len(chunks)}"
)


print("Loading embedding model...")

embedding_model = EmbeddingModel()


print("Generating embeddings...")

texts = [
    chunk.text
    for chunk in chunks
]

embeddings = (
    embedding_model.embed_documents(
        texts
    )
)


dimension = embeddings.shape[1]


print(
    f"Embedding dimension: {dimension}"
)


store = VectorStore(
    dimension=dimension
)


store.add(
    embeddings=embeddings,
    chunks=chunks,
)


store.save(
    INDEX_DIRECTORY
)


print("Vector index created.")