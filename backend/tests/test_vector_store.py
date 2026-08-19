import pytest

from app.services.vector_store import VectorStore


def test_add_and_search_document():
    store = VectorStore()

    store.add(
        "Novixa builds AI systems.",
        [1.0, 0.0, 0.0],
    )

    results = store.search(
        [1.0, 0.0, 0.0],
        top_k=1,
    )

    assert len(results) == 1
    assert results[0].text == "Novixa builds AI systems."


def test_search_returns_most_similar_document_first():
    store = VectorStore()

    store.add(
        "Engineering documentation.",
        [1.0, 0.0, 0.0],
    )

    store.add(
        "Research documentation.",
        [0.0, 1.0, 0.0],
    )

    results = store.search(
        [0.9, 0.1, 0.0],
        top_k=2,
    )

    assert results[0].text == "Engineering documentation."
    assert results[1].text == "Research documentation."


def test_empty_text_is_rejected():
    store = VectorStore()

    with pytest.raises(ValueError):
        store.add("", [1.0, 0.0])


def test_empty_embedding_is_rejected():
    store = VectorStore()

    with pytest.raises(ValueError):
        store.add("Novixa", [])


def test_empty_query_embedding_is_rejected():
    store = VectorStore()

    with pytest.raises(ValueError):
        store.search([])


def test_invalid_top_k_is_rejected():
    store = VectorStore()

    with pytest.raises(ValueError):
        store.search([1.0, 0.0], top_k=0)


def test_mismatched_dimensions_are_rejected():
    store = VectorStore()

    store.add(
        "Novixa",
        [1.0, 0.0],
    )

    with pytest.raises(ValueError):
        store.search([1.0, 0.0, 0.0])


def test_zero_vector_is_rejected():
    store = VectorStore()

    store.add(
        "Novixa",
        [1.0, 0.0],
    )

    with pytest.raises(ValueError):
        store.search([0.0, 0.0])