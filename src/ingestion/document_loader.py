from pathlib import Path
from typing import List

import docx
from pypdf import PdfReader

from src.config.settings import (
    DATASET_DIR,
    IGNORED_DIRECTORIES,
    SUPPORTED_EXTENSIONS,
)


class DocumentLoader:
    """Loads supported documents from the dataset directory."""

    def __init__(self, dataset_directory: Path = DATASET_DIR) -> None:
        self.dataset_directory = dataset_directory

    def discover_documents(self) -> List[Path]:
        """Return all supported documents excluding ignored folders."""

        documents: List[Path] = []

        for file_path in self.dataset_directory.rglob("*"):
            if not file_path.is_file():
                continue

            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            if any(
                ignored in file_path.parts
                for ignored in IGNORED_DIRECTORIES
            ):
                continue

            documents.append(file_path)

        return sorted(documents)

    def extract_text(self, file_path: Path) -> str:
        """Extract text from a supported document."""

        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            return self._read_pdf(file_path)

        if suffix == ".docx":
            return self._read_docx(file_path)

        if suffix == ".txt":
            return self._read_txt(file_path)

        raise ValueError(f"Unsupported file type: {suffix}")

    @staticmethod
    def _read_pdf(file_path: Path) -> str:
        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return "\n".join(pages).strip()

    @staticmethod
    def _read_docx(file_path: Path) -> str:
        document = docx.Document(file_path)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs).strip()

    @staticmethod
    def _read_txt(file_path: Path) -> str:
        return file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).strip()