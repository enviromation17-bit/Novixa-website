import pytest

from app.services.document_chunker import chunk_text


def test_empty_text_returns_no_chunks():
    assert chunk_text("") == []


def test_short_text_returns_one_chunk():
    text = "Novixa builds intelligent software."

    chunks = chunk_text(
        text,
        chunk_size=100,
        overlap=20,
    )

    assert chunks == [text]


def test_text_is_split_into_chunks():
    text = "abcdefghijklmnopqrstuvwxyz"

    chunks = chunk_text(
        text,
        chunk_size=10,
        overlap=2,
    )

    assert chunks == [
        "abcdefghij",
        "ijklmnopqr",
        "qrstuvwxyz",
    ]


def test_chunks_preserve_overlap():
    text = "abcdefghijklmnopqrstuvwxyz"

    chunks = chunk_text(
        text,
        chunk_size=10,
        overlap=2,
    )

    assert chunks[0][-2:] == chunks[1][:2]
    assert chunks[1][-2:] == chunks[2][:2]


def test_invalid_chunk_size_raises_error():
    with pytest.raises(ValueError):
        chunk_text("Novixa", chunk_size=0)


def test_negative_overlap_raises_error():
    with pytest.raises(ValueError):
        chunk_text("Novixa", chunk_size=10, overlap=-1)


def test_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ValueError):
        chunk_text("Novixa", chunk_size=10, overlap=10)