from pathlib import Path
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
DATASET_DIR = DATA_DIR / "dataset"
VECTOR_DB_DIR = DATA_DIR / "vectordb"
MEMORY_DIR = DATA_DIR / "memory"

# Vector database
CHROMA_COLLECTION_NAME = "novatech_policies"

# Memory
SQLITE_DB_PATH = MEMORY_DIR / "novatech_memory.db"

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# LangSmith
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
LANGSMITH_PROJECT = os.getenv(
    "LANGSMITH_PROJECT",
    "NovaTech_Support_Platform",
)
LANGSMITH_TRACING = os.getenv(
    "LANGSMITH_TRACING",
    "false",
).lower() == "true"

# Models
CHAT_MODEL = "gemini-3.1-flash-lite"
EMBEDDING_MODEL = "gemini-embedding-001"

# Retrieval
TOP_K_RESULTS = 3
EMBEDDING_BATCH_SIZE = 50
MIN_CHUNK_LENGTH = 50

# Supported document types
SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}

# Folder names to ignore during indexing
IGNORED_DIRECTORIES = {
    "outdated",
}