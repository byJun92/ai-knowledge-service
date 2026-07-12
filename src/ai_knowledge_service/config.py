from functools import lru_cache
from typing import Literal

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["local", "test", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LogFormat = Literal["console", "json"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AIKS_",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "ai-knowledge-service"
    environment: Environment = "local"
    log_level: LogLevel = "INFO"
    log_format: LogFormat = "console"
    external_api_key: SecretStr | None = None

    @field_validator("app_name")
    @classmethod
    def validate_app_name(cls, value: str) -> str:
        normalized = value.strip()

        if not normalized:
            raise ValueError("app_name must not be blank")

        return normalized


@lru_cache
def get_settings() -> Settings:
    return Settings()


def clear_settings() -> None:
    get_settings.cache_clear()
