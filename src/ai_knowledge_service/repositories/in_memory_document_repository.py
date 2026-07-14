from ai_knowledge_service.domain.document import Document
from ai_knowledge_service.types import DocumentId


class InMemoryDocumentRepository:
    def __init__(self) -> None:
        self._documents: dict[DocumentId, Document] = {}

    def save(self, document: Document) -> None:
        self._documents[document.document_id] = document

    def find_by_id(self, document_id: DocumentId) -> Document | None:
        return self._documents.get(document_id)

    def list_all(self) -> tuple[Document, ...]:
        return tuple(self._documents.values())
