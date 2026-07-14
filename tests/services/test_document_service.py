import pytest

from ai_knowledge_service.domain.document import Document, DocumentType
from ai_knowledge_service.exceptions import (
    DocumentAlreadyExistsError,
    DocumentNotFoundError,
    InvalidDocumentError,
)
from ai_knowledge_service.services.document_service import DocumentService
from ai_knowledge_service.types import DocumentId


def test_register_and_get_document(
    document_service: DocumentService,
) -> None:
    created = document_service.register(
        document_id="doc-001",
        title="Dependency Inversion",
        source_url="https://example.com/dependency-inversion",
        document_type=DocumentType.TECH_ARTICLE,
    )

    assert document_service.get("doc-001") is created


def test_register_rejects_duplicate_document(
    document_service: DocumentService,
) -> None:
    document_service.register(
        document_id="doc-001",
        title="First",
        source_url="https://example.com/first",
        document_type=DocumentType.TECH_ARTICLE,
    )

    with pytest.raises(DocumentAlreadyExistsError):
        document_service.register(
            document_id="doc-001",
            title="Duplicate",
            source_url="https://example.com/duplicate",
            document_type=DocumentType.TECH_ARTICLE,
        )


def test_register_converts_domain_error(
    document_service: DocumentService,
) -> None:
    with pytest.raises(InvalidDocumentError):
        document_service.register(
            document_id="",
            title="Invalid",
            source_url="https://example.com/invalid",
            document_type=DocumentType.TECH_ARTICLE,
        )


def test_get_raises_when_document_does_not_exist(
    document_service: DocumentService,
) -> None:
    with pytest.raises(DocumentNotFoundError):
        document_service.get("missing")


def test_list_documents(
    document_service: DocumentService,
) -> None:
    first = document_service.register(
        document_id="doc-001",
        title="First",
        source_url="https://example.com/first",
        document_type=DocumentType.TECH_ARTICLE,
    )
    second = document_service.register(
        document_id="doc-002",
        title="Second",
        source_url="https://example.com/second",
        document_type=DocumentType.DOCUMENTATION,
    )

    assert document_service.list_documents() == (first, second)


class RecordingDocumentRepository:
    def __init__(self) -> None:
        self.saved: list[Document] = []

    def save(self, document: Document) -> None:
        self.saved.append(document)

    def find_by_id(self, document_id: DocumentId) -> Document | None:
        for document in self.saved:
            if document.document_id == document_id:
                return document
        return None

    def list_all(self) -> tuple[Document, ...]:
        return tuple(self.saved)


def test_service_accepts_non_inheriting_fake() -> None:
    repository = RecordingDocumentRepository()
    service = DocumentService(repository)

    created = service.register(
        document_id="doc-001",
        title="Structural Typing",
        source_url="https://example.com/structural-typing",
        document_type=DocumentType.TECH_ARTICLE,
    )

    assert repository.saved == [created]
