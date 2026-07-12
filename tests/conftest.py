from pathlib import Path

import pytest

from ai_knowledge_service.config import Settings


@pytest.fixture
def test_settings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Settings:
    monkeypatch.chdir(tmp_path)

    return Settings(environment="test", log_level="DEBUG", log_format="json")
