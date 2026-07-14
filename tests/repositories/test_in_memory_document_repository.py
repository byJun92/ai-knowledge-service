from ai_knowledge_service.domain.document import Document, DocumentType
from ai_knowledge_service.repositories.in_memory_document_repository import (
    InMemoryDocumentRepository,
)
from ai_knowledge_service.types import DocumentId


def test_save_and_find_document() -> None:
    repository = InMemoryDocumentRepository()
    document = Document.create(
        document_id="doc-001",
        title="Repository Pattern",
        source_url="https://example.com/repository-pattern",
        document_type=DocumentType.TECH_ARTICLE,
    )

    repository.save(document)

    assert repository.find_by_id(document.document_id) is document


def test_list_all_documents() -> None:
    repository = InMemoryDocumentRepository()
    first = Document.create(
        document_id="doc-001",
        title="First",
        source_url="https://example.com/first",
        document_type=DocumentType.TECH_ARTICLE,
    )
    second = Document.create(
        document_id="doc-002",
        title="Second",
        source_url="https://example.com/second",
        document_type=DocumentType.DOCUMENTATION,
    )

    repository.save(first)
    repository.save(second)

    assert repository.list_all() == (first, second)


def test_find_returns_none_when_document_does_not_exist() -> None:
    repository = InMemoryDocumentRepository()

    assert repository.find_by_id(DocumentId("missing")) is None
