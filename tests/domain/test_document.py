import pytest

from ai_knowledge_service.domain.document import Document, DocumentType


def test_create_document() -> None:
    document = Document.create(
        document_id="paper-001",
        title="Retrieval-Augmented Generation",
        source_url="https://example.com/paper",
        document_type=DocumentType.PAPER,
    )

    assert document.document_id == "paper-001"
    assert document.title == "Retrieval-Augmented Generation"
    assert document.document_type is DocumentType.PAPER
    assert document.collected_at.tzinfo is not None


@pytest.mark.parametrize(
    ("document_id", "title", "source_url", "expected_message"),
    [
        ("", "Valid title", "https://example.com", "document_id"),
        ("doc-1", " ", "https://example.com", "title"),
        ("doc-1", "Valid title", "ftp://example.com", "source_url"),
    ],
)
def test_create_document_rejects_invalid_input(
    document_id: str,
    title: str,
    source_url: str,
    expected_message: str,
) -> None:
    with pytest.raises(ValueError, match=expected_message):
        Document.create(
            document_id=document_id,
            title=title,
            source_url=source_url,
            document_type=DocumentType.DOCUMENTATION,
        )
