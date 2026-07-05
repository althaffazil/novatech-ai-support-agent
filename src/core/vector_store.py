from typing import List

import chromadb

from src.config.settings import (
    CHROMA_COLLECTION_NAME,
    TOP_K_RESULTS,
    VECTOR_DB_DIR,
)
from src.ingestion.knowledge_base_builder import KnowledgeChunk


class VectorStore:
    """Manages the ChromaDB knowledge base."""

    def __init__(
        self,
        recreate_collection: bool = False,
    ) -> None:

        self.client = chromadb.PersistentClient(
            path=str(VECTOR_DB_DIR),
        )

        self.collection = self._get_collection(
            recreate_collection,
        )

        if (
            not recreate_collection
            and self.collection.count() == 0
        ):
            raise RuntimeError(
                "\n"
                "Knowledge base has not been built.\n\n"
                "Run the following command first:\n\n"
                "python build_knowledge_base.py\n"
            )

    def _get_collection(
        self,
        recreate: bool,
    ):

        if recreate:

            try:
                self.client.delete_collection(
                    CHROMA_COLLECTION_NAME,
                )
            except Exception:
                pass

            return self.client.create_collection(
                name=CHROMA_COLLECTION_NAME,
            )

        try:
            return self.client.get_collection(
                CHROMA_COLLECTION_NAME,
            )

        except Exception:

            return self.client.create_collection(
                name=CHROMA_COLLECTION_NAME,
            )

    def add_documents(
        self,
        chunks: List[KnowledgeChunk],
        embeddings: List[List[float]],
    ) -> None:

        self.collection.add(
            ids=[
                f"chunk_{i}"
                for i in range(len(chunks))
            ],
            documents=[
                chunk.text
                for chunk in chunks
            ],
            embeddings=embeddings,
            metadatas=[
                {
                    "source": chunk.source,
                    "chunk_id": chunk.chunk_id,
                }
                for chunk in chunks
            ],
        )

    def search(
        self,
        query_embedding: List[float],
        top_k: int = TOP_K_RESULTS,
    ):

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

    def count(self) -> int:
        return self.collection.count()