from pathlib import Path

import pytest

from ai_knowledge_service.config import Settings
from ai_knowledge_service.repositories.in_memory_document_repository import (
    InMemoryDocumentRepository,
)
from ai_knowledge_service.services.document_service import DocumentService


@pytest.fixture
def test_settings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Settings:
    monkeypatch.chdir(tmp_path)

    return Settings(environment="test", log_level="DEBUG", log_format="json")


@pytest.fixture
def document_repository() -> InMemoryDocumentRepository:
    return InMemoryDocumentRepository()


@pytest.fixture
def document_service(
    document_repository: InMemoryDocumentRepository,
) -> DocumentService:
    return DocumentService(document_repository)
