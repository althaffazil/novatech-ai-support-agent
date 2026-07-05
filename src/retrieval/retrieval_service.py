from src.config.settings import TOP_K_RESULTS
from src.core.embeddings import EmbeddingService
from src.core.vector_store import VectorStore


class RetrievalService:
    """Provides semantic search over the NovaTech knowledge base."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def search(
        self,
        query: str,
        top_k: int = TOP_K_RESULTS,
    ) -> str:
        """
        Search the knowledge base and return formatted context.
        """

        query_embedding = self.embedding_service.generate_embedding(
            query
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        documents = results["documents"][0]
        metadata = results["metadatas"][0]

        if not documents:
            return "No relevant policy information found."

        context = ["--- RETRIEVED POLICIES ---"]

        for document, meta in zip(documents, metadata):
            context.append(
                f"[Source: {meta['source']}]\n{document}"
            )

        return "\n\n".join(context)