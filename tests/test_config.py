from pathlib import Path

import pytest
from pydantic import SecretStr, ValidationError

from ai_knowledge_service.config import Settings


def test_settings_load_prefixed_environment_variables(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("AIKS_ENVIRONMENT", "test")
    monkeypatch.setenv("AIKS_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("AIKS_LOG_FORMAT", "json")

    settings = Settings()

    assert settings.environment == "test"
    assert settings.log_level == "DEBUG"
    assert settings.log_format == "json"


def test_settings_reject_invalid_environment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("AIKS_ENVIRONMENT", "invalid")

    with pytest.raises(ValidationError):
        Settings()


def test_secret_is_masked() -> None:
    settings = Settings(
        external_api_key=SecretStr("test-secret"),
    )

    assert settings.external_api_key is not None
    assert str(settings.external_api_key) == "**********"
    assert settings.external_api_key.get_secret_value() == "test-secret"
    assert "test-secret" not in repr(settings)