from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(
        self,
        model_name="BAAI/bge-small-en-v1.5",
    ):

        print(
            f"Loading embedding model: {model_name}"
        )

        self.model = SentenceTransformer(
            model_name
        )

    def embed_documents(
        self,
        documents: list[str],
    ):

        return self.model.encode(
            documents,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

    def embed_query(
        self,
        query: str,
    ):

        return self.model.encode(
            [query],
            normalize_embeddings=True,
        )[0]