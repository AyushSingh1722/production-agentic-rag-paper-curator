import asyncio
import logging
from typing import List

import httpx
from src.schemas.embeddings.jina import JinaEmbeddingRequest, JinaEmbeddingResponse

logger = logging.getLogger(__name__)


class JinaEmbeddingsClient:
    """Client for Jina AI embeddings API.

    Uses Jina embeddings v3 model with 1024 dimensions optimized for retrieval.
    Documentation: https://jina.ai/embeddings
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.jina.ai/v1",
        max_retries: int = 5,
        base_backoff_seconds: float = 2.0,
    ):
        """Initialize Jina embeddings client.

        :param api_key: Jina API key
        :param base_url: API base URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.client = httpx.AsyncClient(timeout=30.0)
        self.max_retries = max_retries
        self.base_backoff_seconds = base_backoff_seconds
        logger.info("Jina embeddings client initialized")

    def _retry_delay(self, response: httpx.Response | None, attempt: int) -> float:
        """Compute retry delay, preferring server guidance when available."""
        if response is not None:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    return max(float(retry_after), 0.0)
                except ValueError:
                    logger.debug(f"Ignoring non-numeric Retry-After header: {retry_after}")

        return self.base_backoff_seconds * (2 ** attempt)

    async def _post_embeddings(self, request_data: JinaEmbeddingRequest, request_label: str) -> JinaEmbeddingResponse:
        """Post embeddings request with retry/backoff for transient failures."""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.post(
                    f"{self.base_url}/embeddings",
                    headers=self.headers,
                    json=request_data.model_dump(),
                )
                response.raise_for_status()
                return JinaEmbeddingResponse(**response.json())

            except httpx.HTTPStatusError as e:
                last_exception = e
                status_code = e.response.status_code
                is_retryable = status_code == 429 or 500 <= status_code < 600

                if not is_retryable or attempt >= self.max_retries:
                    logger.error(f"Error embedding {request_label}: {e}")
                    raise

                delay = self._retry_delay(e.response, attempt)
                logger.warning(
                    f"Retryable Jina error while embedding {request_label} "
                    f"(status={status_code}, attempt={attempt + 1}/{self.max_retries + 1}). "
                    f"Retrying in {delay:.1f}s."
                )
                await asyncio.sleep(delay)

            except httpx.RequestError as e:
                last_exception = e
                if attempt >= self.max_retries:
                    logger.error(f"Network error embedding {request_label}: {e}")
                    raise

                delay = self._retry_delay(None, attempt)
                logger.warning(
                    f"Transient network error while embedding {request_label} "
                    f"(attempt={attempt + 1}/{self.max_retries + 1}). Retrying in {delay:.1f}s."
                )
                await asyncio.sleep(delay)

            except Exception as e:
                logger.error(f"Unexpected error embedding {request_label}: {e}")
                raise

        if last_exception:
            raise last_exception

    async def embed_passages(self, texts: List[str], batch_size: int = 20) -> List[List[float]]:
        """Embed text passages for indexing.

        :param texts: List of text passages to embed
        :param batch_size: Number of texts to process in each API call
        :returns: List of embedding vectors
        """
        embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]

            request_data = JinaEmbeddingRequest(
                model="jina-embeddings-v3", task="retrieval.passage", dimensions=1024, input=batch
            )

            try:
                result = await self._post_embeddings(request_data, f"{len(batch)} passages")
                batch_embeddings = [item["embedding"] for item in result.data]
                embeddings.extend(batch_embeddings)

                logger.debug(f"Embedded batch of {len(batch)} passages")

                # Small pause helps avoid hammering the embeddings API during bulk indexing.
                if i + batch_size < len(texts):
                    await asyncio.sleep(0.25)

            except httpx.HTTPError as e:
                logger.error(f"Error embedding passages: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error in embed_passages: {e}")
                raise

        logger.info(f"Successfully embedded {len(texts)} passages")
        return embeddings

    async def embed_query(self, query: str) -> List[float]:
        """Embed a search query.

        :param query: Query text to embed
        :returns: Embedding vector for the query
        """
        request_data = JinaEmbeddingRequest(model="jina-embeddings-v3", task="retrieval.query", dimensions=1024, input=[query])

        try:
            result = await self._post_embeddings(request_data, "query")
            embedding = result.data[0]["embedding"]

            logger.debug(f"Embedded query: '{query[:50]}...'")
            return embedding

        except httpx.HTTPError as e:
            logger.error(f"Error embedding query: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in embed_query: {e}")
            raise

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
