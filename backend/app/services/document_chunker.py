"""Utilities for splitting documents into retrieval-friendly text chunks."""


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Source document text.
        chunk_size: Maximum number of characters per chunk.
        overlap: Number of characters shared between adjacent chunks.

    Returns:
        A list of text chunks in their original order.

    Raises:
        ValueError: If chunk_size or overlap values are invalid.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    if not text:
        return []

    chunks: list[str] = []
    start = 0
    step = chunk_size - overlap

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start += step

    return chunks