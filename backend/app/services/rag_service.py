"""Retrieval-Augmented Generation service for Novixa."""

from app.services.document_chunker import chunk_text
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore


class RAGService:
    """Coordinate document chunking, embedding, storage, and retrieval."""

    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
        vector_store: VectorStore | None = None,
    ) -> None:
        self.embedding_service = (
            embedding_service or EmbeddingService()
        )
        self.vector_store = (
            vector_store or VectorStore()
        )

    def ingest_document(
        self,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200,
    ) -> int:
        """Chunk and embed a document, returning the number of chunks."""

        if not text.strip():
            raise ValueError("text cannot be empty")

        chunks = chunk_text(
            text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for chunk in chunks:
            embedding = self.embedding_service.embed_text(chunk)

            self.vector_store.add(
                text=chunk,
                embedding=embedding,
            )

        return len(chunks)

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[str]:
        """Retrieve the most relevant document chunks."""

        if not query.strip():
            raise ValueError("query cannot be empty")

        query_embedding = self.embedding_service.embed_text(query)

        documents = self.vector_store.search(
            query_embedding,
            top_k=top_k,
        )

        return [
            document.text
            for document in documents
        ]