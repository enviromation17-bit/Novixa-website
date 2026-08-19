from app.services.rag_service import RAGService


class FakeEmbeddingService:
    def embed_text(self, text):
        if "engineering" in text.lower():
            return [1.0, 0.0, 0.0]

        return [0.0, 1.0, 0.0]


def test_ingest_document():
    service = RAGService(
        embedding_service=FakeEmbeddingService()
    )

    count = service.ingest_document(
        "Engineering documentation.",
        chunk_size=100,
        overlap=20,
    )

    assert count == 1


def test_retrieve_returns_relevant_chunks():
    service = RAGService(
        embedding_service=FakeEmbeddingService()
    )

    service.ingest_document(
        "Engineering documentation.",
        chunk_size=100,
        overlap=20,
    )

    service.ingest_document(
        "Research documentation.",
        chunk_size=100,
        overlap=20,
    )

    results = service.retrieve(
        "engineering",
        top_k=1,
    )

    assert len(results) == 1
    assert results[0] == "Engineering documentation."


def test_empty_document_is_rejected():
    service = RAGService(
        embedding_service=FakeEmbeddingService()
    )

    try:
        service.ingest_document("")
        assert False
    except ValueError:
        assert True


def test_empty_query_is_rejected():
    service = RAGService(
        embedding_service=FakeEmbeddingService()
    )

    try:
        service.retrieve("")
        assert False
    except ValueError:
        assert True