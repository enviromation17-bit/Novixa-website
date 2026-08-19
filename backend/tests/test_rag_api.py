from fastapi.testclient import TestClient

from app.main import app
from app.routes.v1 import rag


client = TestClient(app)


class FakeRAGService:
    def ingest_document(self, text: str) -> int:
        assert text == "Novixa builds intelligent software."
        return 1

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[str]:
        assert query == "Novixa"
        assert top_k == 2

        return [
            "Novixa builds intelligent software."
        ]


def test_ingest_document_endpoint():
    original_service = rag.rag_service

    try:
        rag.rag_service = FakeRAGService()

        response = client.post(
            "/api/v1/rag/ingest",
            params={
                "text": "Novixa builds intelligent software."
            },
        )

        assert response.status_code == 200
        assert response.json() == {
            "success": True,
            "chunks_created": 1,
        }

    finally:
        rag.rag_service = original_service


def test_search_documents_endpoint():
    original_service = rag.rag_service

    try:
        rag.rag_service = FakeRAGService()

        response = client.get(
            "/api/v1/rag/search",
            params={
                "query": "Novixa",
                "top_k": 2,
            },
        )

        assert response.status_code == 200
        assert response.json() == {
            "query": "Novixa",
            "results": [
                "Novixa builds intelligent software."
            ],
        }

    finally:
        rag.rag_service = original_service