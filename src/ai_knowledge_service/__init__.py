from ai_knowledge_service.config import get_settings
from ai_knowledge_service.observability.logging import configure_logging, get_logger


def main() -> None:
    settings = get_settings()
    configure_logging(settings)

    logger = get_logger(__name__)
    logger.info(
        "application_started",
        app_name=settings.app_name,
        environment=settings.environment,
    )
