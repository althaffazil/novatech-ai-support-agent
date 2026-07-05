from typing import List

from src.config.settings import MIN_CHUNK_LENGTH


class DocumentChunker:
    """Splits extracted document text into searchable chunks."""

    def __init__(self, min_chunk_length: int = MIN_CHUNK_LENGTH) -> None:
        self.min_chunk_length = min_chunk_length

    def chunk(self, text: str) -> List[str]:
        """
        Split a document into paragraph-based chunks.
        """

        if not text.strip():
            return []

        chunks = [
            chunk.strip()
            for chunk in text.split("\n\n")
            if len(chunk.strip()) >= self.min_chunk_length
        ]

        return chunks