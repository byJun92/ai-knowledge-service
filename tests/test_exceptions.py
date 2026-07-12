from ai_knowledge_service.exceptions import DocumentNotFoundError


def test_application_error_can_be_serialized() -> None:
    error = DocumentNotFoundError(
        "Document was not found",
        details={"document_id": "doc-001"},
    )

    assert error.to_dict() == {
        "code": "document_not_found",
        "message": "Document was not found",
        "details": {
            "document_id": "doc-001",
        },
    }