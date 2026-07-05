from src.config.logging_config import configure_logging
from src.ingestion.knowledge_base_indexer import (
    KnowledgeBaseIndexer,
)


def main() -> None:

    configure_logging()

    indexer = KnowledgeBaseIndexer()

    indexer.build()


if __name__ == "__main__":
    main()