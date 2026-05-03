import asyncio
import logging

from src.config import get_settings
from src.services.cache.factory import make_cache_client
from src.services.embeddings.factory import make_embeddings_service
from src.services.langfuse.factory import make_langfuse_tracer
from src.services.ollama.factory import make_ollama_client
from src.services.opensearch.factory import make_opensearch_client
from src.services.telegram.factory import make_telegram_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Run Telegram bot as a dedicated single-process service."""
    settings = get_settings()

    if not settings.telegram.enabled:
        logger.info("Telegram bot is disabled")
        return

    opensearch_client = make_opensearch_client()
    embeddings_service = make_embeddings_service()
    ollama_client = make_ollama_client()
    cache_client = make_cache_client(settings)
    langfuse_tracer = make_langfuse_tracer()

    telegram_service = make_telegram_service(
        opensearch_client=opensearch_client,
        embeddings_client=embeddings_service,
        ollama_client=ollama_client,
        cache_client=cache_client,
        langfuse_tracer=langfuse_tracer,
    )

    if not telegram_service:
        logger.info("Telegram bot not configured - exiting")
        return

    await telegram_service.start()
    logger.info("Telegram bot runner is active")

    try:
        await asyncio.Event().wait()
    finally:
        await telegram_service.stop()
        logger.info("Telegram bot runner stopped")


if __name__ == "__main__":
    asyncio.run(main())
