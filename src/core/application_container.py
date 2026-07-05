from __future__ import annotations

from typing import Optional

from src.config.settings import SQLITE_DB_PATH
from src.core.embeddings import EmbeddingService
from src.core.vector_store import VectorStore
from src.graph.workflow import CustomerSupportWorkflow
from src.memory.sqlite_checkpoint import SqliteCheckpointManager
from src.retrieval.retrieval_service import RetrievalService
from src.services.chat_service import ChatService


class ApplicationContainer:
    """Singleton responsible for creating and owning application services."""

    _instance: Optional["ApplicationContainer"] = None

    def __new__(cls) -> "ApplicationContainer":

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False

        return cls._instance

    def __init__(self) -> None:

        if self._initialized:
            return

        embedding_service = EmbeddingService()

        vector_store = VectorStore()

        retrieval_service = RetrievalService(
            embedding_service=embedding_service,
            vector_store=vector_store,
        )

        checkpoint_manager = SqliteCheckpointManager(
            SQLITE_DB_PATH,
        )

        workflow = CustomerSupportWorkflow(
            retrieval_service=retrieval_service,
            checkpoint_manager=checkpoint_manager,
        ).build()

        self.chat_service = ChatService(
            workflow=workflow,
        )

        self._initialized = True