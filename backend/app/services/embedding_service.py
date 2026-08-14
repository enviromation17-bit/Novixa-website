"""Embedding service for the Novixa RAG pipeline."""

from google import genai


class EmbeddingService:
    """Generate vector embeddings for text."""

    def __init__(
        self,
        model: str = "gemini-embedding-001",
        client=None,
    ) -> None:
        self.model = model
        self.client = client or genai.Client()

    def embed_text(self, text: str) -> list[float]:
        """Generate an embedding vector for a single text."""

        if not text.strip():
            raise ValueError("text cannot be empty")

        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
        )

        if not response.embeddings:
            raise RuntimeError("Embedding response contained no embeddings")

        values = response.embeddings[0].values

        if values is None:
            raise RuntimeError("Embedding response contained no vector values")

        return list(values)
