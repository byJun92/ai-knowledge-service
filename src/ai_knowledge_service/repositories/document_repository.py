from typing import Protocol

from ai_knowledge_service.domain.document import Document
from ai_knowledge_service.types import DocumentId


class DocumentRepository(Protocol):
    def save(self, document: Document) -> None: ...

    def find_by_id(self, document_id: DocumentId) -> Document | None: ...

    def list_all(self) -> tuple[Document, ...]: ...
