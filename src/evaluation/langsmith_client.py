import os

from langsmith import Client

from src.config.settings import (
    LANGSMITH_API_KEY,
    LANGSMITH_PROJECT,
    LANGSMITH_TRACING,
)


class LangSmithClientFactory:
    """Creates the LangSmith client and configures tracing."""

    def __init__(self) -> None:

        os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
        os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
        os.environ["LANGSMITH_TRACING"] = (
            "true" if LANGSMITH_TRACING else "false"
        )

        self.client = Client()

    def get_client(self) -> Client:
        return self.client