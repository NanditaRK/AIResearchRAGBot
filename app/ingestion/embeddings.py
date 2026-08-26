from sentence_transformers import SentenceTransformer

from app import config


model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5",
    token=config.HF_TOKEN,
)


def embed_texts(texts: list[str]) -> list[list[float]]:

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    )
    
    return embeddings.tolist()