from ai_knowledge_service.domain.document import Document, DocumentType
from ai_knowledge_service.exceptions import (
    DocumentAlreadyExistsError,
    DocumentNotFoundError,
    InvalidDocumentError,
)
from ai_knowledge_service.observability.logging import get_logger
from ai_knowledge_service.repositories.document_repository import DocumentRepository
from ai_knowledge_service.types import DocumentId


class DocumentService:
    def __init__(self, repository: DocumentRepository) -> None:
        self._repository = repository
        self._logger = get_logger(__name__)

    def register(
        self,
        *,
        document_id: str,
        title: str,
        source_url: str,
        document_type: DocumentType,
    ) -> Document:
        try:
            document = Document.create(
                document_id=document_id,
                title=title,
                source_url=source_url,
                document_type=document_type,
            )
        except ValueError as error:
            raise InvalidDocumentError(
                str(error),
                details={"document_id": document_id},
            ) from error

        existing = self._repository.find_by_id(document.document_id)

        if existing is not None:
            raise DocumentAlreadyExistsError(
                "Document already exists",
                details={"document_id": str(document.document_id)},
            )

        self._repository.save(document)

        self._logger.info(
            "document_registered",
            document_id=str(document.document_id),
            document_type=document.document_type.value,
        )

        return document

    def get(self, document_id: str) -> Document:
        normalized_id = document_id.strip()

        if not normalized_id:
            raise InvalidDocumentError(
                "document_id must not be blank",
                details={"document_id": document_id},
            )

        document = self._repository.find_by_id(DocumentId(normalized_id))

        if document is None:
            raise DocumentNotFoundError(
                "Document was not found",
                details={"document_id": normalized_id},
            )

        return document

    def list_documents(self) -> tuple[Document, ...]:
        return self._repository.list_all()
