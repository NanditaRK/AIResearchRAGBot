from .embeddings import EmbeddingModel
from .vector_store import VectorStore
from .llm import LLM


class RAG:

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_model: EmbeddingModel,
    ):

        self.vector_store = vector_store
        self.embedding_model = embedding_model

        self.llm = LLM()

    def answer(
        self,
        question: str,
        top_k: int = 5,
    ):

        # 1. Convert question into embedding
        query_embedding = (
            self.embedding_model.embed_query(
                question
            )
        )

        # 2. Search vector database
        results = self.vector_store.search(
            query_embedding,
            k=top_k,
        )

        # 3. Build context
        context_parts = []

        sources = []

        for result in results:

            chunk = result["chunk"]

            context_parts.append(
                f"""
[source: {chunk.source}]

{chunk.text}
"""
            )

            sources.append(
                {
                    "source": chunk.source,
                    "chunk_id": chunk.chunk_id,
                    "score": result["score"],
                }
            )

        context = "\n".join(
            context_parts
        )

        # 4. Ask LLM
        answer = self.llm.generate(
            question=question,
            context=context,
        )

        return {
            "answer": answer,
            "sources": sources,
        }