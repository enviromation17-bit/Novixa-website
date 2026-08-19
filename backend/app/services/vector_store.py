"""In-memory vector store for the Novixa RAG pipeline."""

from dataclasses import dataclass


@dataclass
class VectorDocument:
    text: str
    embedding: list[float]


class VectorStore:
    """Store document embeddings and perform cosine-similarity search."""

    def __init__(self) -> None:
        self._documents: list[VectorDocument] = []

    def add(
        self,
        text: str,
        embedding: list[float],
    ) -> None:
        if not text.strip():
            raise ValueError("text cannot be empty")

        if not embedding:
            raise ValueError("embedding cannot be empty")

        self._documents.append(
            VectorDocument(
                text=text,
                embedding=list(embedding),
            )
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3,
    ) -> list[VectorDocument]:
        if not query_embedding:
            raise ValueError("query_embedding cannot be empty")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")

        scored = [
            (
                self._cosine_similarity(
                    query_embedding,
                    document.embedding,
                ),
                document,
            )
            for document in self._documents
        ]

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            document
            for _, document in scored[:top_k]
        ]

    @staticmethod
    def _cosine_similarity(
        first: list[float],
        second: list[float],
    ) -> float:
        if len(first) != len(second):
            raise ValueError(
                "embedding dimensions must match"
            )

        first_norm = sum(value * value for value in first) ** 0.5
        second_norm = sum(value * value for value in second) ** 0.5

        if first_norm == 0 or second_norm == 0:
            raise ValueError(
                "embedding vectors cannot have zero magnitude"
            )

        dot_product = sum(
            left * right
            for left, right in zip(first, second)
        )

        return dot_product / (first_norm * second_norm)