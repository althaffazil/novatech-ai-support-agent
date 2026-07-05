from pathlib import Path
import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver


class SqliteCheckpointManager:
    """Creates and manages the LangGraph SQLite checkpointer."""

    def __init__(self, database_path: Path) -> None:
        database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.connection = sqlite3.connect(
            database_path,
            check_same_thread=False,
        )

        self.checkpointer = SqliteSaver(
            self.connection,
        )

    def get_checkpointer(self) -> SqliteSaver:
        return self.checkpointer

    def close(self) -> None:
        self.connection.close()