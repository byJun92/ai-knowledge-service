from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Self

from ai_knowledge_service.types import DocumentId


class DocumentType(StrEnum):
    PAPER = "paper"
    TECH_ARTICLE = "tech_article"
    DOCUMENTATION = "documentation"


@dataclass(frozen=True, slots=True)
class Document:
    document_id: DocumentId
    title: str
    source_url: str
    document_type: DocumentType
    collected_at: datetime

    @classmethod
    def create(
        cls, *, document_id: str, title: str, source_url: str, document_type: DocumentType
    ) -> Self:
        normalized_id = document_id.strip()
        normalized_title = title.strip()
        normalized_url = source_url.strip()

        if not normalized_id:
            raise ValueError("document_id must not be blank")
        if not normalized_title:
            raise ValueError("title must not be blank")
        if not normalized_url.startswith(("https://", "http://")):
            raise ValueError("source_url must be an HTTP(S) URL")

        return cls(
            document_id=DocumentId(normalized_id),
            title=normalized_title,
            source_url=normalized_url,
            document_type=document_type,
            collected_at=datetime.now(UTC),
        )
