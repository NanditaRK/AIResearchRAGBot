import pickle
from pathlib import Path

import faiss
import numpy as np

from .chunking import Chunk


class VectorStore:

    def __init__(self, dimension: int):

        self.dimension = dimension

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.chunks: list[Chunk] = []

    def add(
        self,
        embeddings,
        chunks: list[Chunk],
    ):

        embeddings = np.asarray(
            embeddings,
            dtype="float32",
        )

        self.index.add(embeddings)

        self.chunks.extend(chunks)

    def search(
        self,
        query_embedding,
        k: int = 5,
    ):

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32",
        )

        scores, indices = self.index.search(
            query_embedding,
            k,
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):

            if index == -1:
                continue

            results.append(
                {
                    "score": float(score),
                    "chunk": self.chunks[index],
                }
            )

        return results

    def save(self, directory: str):

        directory = Path(directory)

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            str(directory / "index.faiss"),
        )

        with open(
            directory / "chunks.pkl",
            "wb",
        ) as f:

            pickle.dump(
                self.chunks,
                f,
            )

    @classmethod
    def load(
        cls,
        directory: str,
    ):

        directory = Path(directory)

        index = faiss.read_index(
            str(directory / "index.faiss")
        )

        with open(
            directory / "chunks.pkl",
            "rb",
        ) as f:

            chunks = pickle.load(f)

        store = cls(index.d)

        store.index = index
        store.chunks = chunks

        return store