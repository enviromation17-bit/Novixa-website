import pytest

from app.services.embedding_service import EmbeddingService


class FakeEmbedding:
    def __init__(self, values):
        self.values = values


class FakeResponse:
    def __init__(self, embeddings):
        self.embeddings = embeddings


class FakeModels:
    def embed_content(self, *, model, contents):
        assert model == "gemini-embedding-001"
        assert contents == "Novixa AI"

        return FakeResponse(
            embeddings=[
                FakeEmbedding([0.1, 0.2, 0.3])
            ]
        )


class FakeClient:
    def __init__(self):
        self.models = FakeModels()


def test_embed_text_returns_vector():
    service = EmbeddingService(client=FakeClient())

    vector = service.embed_text("Novixa AI")

    assert vector == [0.1, 0.2, 0.3]


def test_embed_text_rejects_empty_text():
    service = EmbeddingService(client=FakeClient())

    with pytest.raises(ValueError):
        service.embed_text("")


def test_embed_text_rejects_whitespace():
    service = EmbeddingService(client=FakeClient())

    with pytest.raises(ValueError):
        service.embed_text("   ")
