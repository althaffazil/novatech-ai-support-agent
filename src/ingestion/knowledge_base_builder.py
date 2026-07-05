from dataclasses import dataclass
from pathlib import Path
from typing import List

from src.ingestion.document_chunker import DocumentChunker
from src.ingestion.document_loader import DocumentLoader


@dataclass(frozen=True)
class KnowledgeChunk:
    text: str
    source: str
    chunk_id: int


class KnowledgeBaseBuilder:
    """Builds searchable knowledge chunks from the dataset."""

    def __init__(
        self,
        loader: DocumentLoader,
        chunker: DocumentChunker,
    ) -> None:
        self.loader = loader
        self.chunker = chunker

    def build(self) -> List[KnowledgeChunk]:
        knowledge_chunks: List[KnowledgeChunk] = []

        documents = self.loader.discover_documents()

        for document in documents:
            raw_text = self.loader.extract_text(document)

            chunks = self.chunker.chunk(raw_text)

            for index, chunk in enumerate(chunks):
                knowledge_chunks.append(
                    KnowledgeChunk(
                        text=chunk,
                        source=document.name,
                        chunk_id=index,
                    )
                )

        return knowledge_chunks