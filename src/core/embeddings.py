from typing import List

from src.config.settings import EMBEDDING_BATCH_SIZE, EMBEDDING_MODEL
from src.core.gemini_client import GeminiClient


class EmbeddingService:
    """Generates embeddings using Gemini."""

    def __init__(self) -> None:
        self.client = GeminiClient.get_client()

    def generate_embedding(self, text: str) -> List[float]:
        """Generate an embedding for a single text."""

        response = self.client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
        )

        return response.embeddings[0].values

    def generate_embeddings(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        """Generate embeddings for multiple texts."""

        if not texts:
            return []

        embeddings: List[List[float]] = []

        for index in range(0, len(texts), EMBEDDING_BATCH_SIZE):
            batch = texts[index:index + EMBEDDING_BATCH_SIZE]

            response = self.client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=batch,
            )

            embeddings.extend(
                embedding.values
                for embedding in response.embeddings
            )

        return embeddings