import logging

from src.core.embeddings import EmbeddingService
from src.core.vector_store import VectorStore
from src.ingestion.document_chunker import DocumentChunker
from src.ingestion.document_loader import DocumentLoader
from src.ingestion.knowledge_base_builder import (
    KnowledgeBaseBuilder,
)

logger = logging.getLogger(__name__)


class KnowledgeBaseIndexer:
    """Builds and indexes the NovaTech knowledge base."""

    def __init__(self) -> None:
        self.loader = DocumentLoader()
        self.chunker = DocumentChunker()

        self.builder = KnowledgeBaseBuilder(
            loader=self.loader,
            chunker=self.chunker,
        )

        self.embedding_service = EmbeddingService()

        self.vector_store = VectorStore(
            recreate_collection=True,
        )

    def build(self) -> None:

        logger.info("Loading documents...")

        chunks = self.builder.build()

        logger.info(
            "Knowledge chunks created: %s",
            len(chunks),
        )

        logger.info("Generating embeddings...")

        embeddings = self.embedding_service.generate_embeddings(
            [chunk.text for chunk in chunks]
        )

        logger.info("Storing embeddings in ChromaDB...")

        self.vector_store.add_documents(
            chunks=chunks,
            embeddings=embeddings,
        )

        logger.info(
            "Knowledge base built successfully."
        )

        logger.info(
            "Indexed chunks: %s",
            self.vector_store.count(),
        )