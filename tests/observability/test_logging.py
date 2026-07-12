import json

import pytest

from ai_knowledge_service.config import Settings
from ai_knowledge_service.observability.logging import configure_logging, get_logger


def test_json_log_contains_searchable_fields(
    test_settings: Settings,
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging(test_settings)
    logger = get_logger("test")

    logger.info(
        "document_processed",
        document_id="doc-001",
        latency_ms=153,
    )

    output = capsys.readouterr().out.strip()
    event = json.loads(output)

    assert event["event"] == "document_processed"
    assert event["document_id"] == "doc-001"
    assert event["latency_ms"] == 153
    assert event["level"] == "info"
    assert event["logger"] == "test"
    assert "timestamp" in event
