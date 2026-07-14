from collections.abc import Mapping
from typing import Any


class ApplicationError(Exception):
    code = "application_error"

    def __init__(
        self,
        message: str,
        *,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.details = dict(details or {})

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


class InvalidDocumentError(ApplicationError):
    code = "invalid_document"


class DocumentNotFoundError(ApplicationError):
    code = "document_not_found"


class ExternalServiceError(ApplicationError):
    code = "external_service_error"


class DocumentAlreadyExistsError(ApplicationError):
    code = "document_already_exists"
