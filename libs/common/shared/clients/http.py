from httpx import AsyncClient


__all__ = [
    "http_client",
]


http_client: AsyncClient = AsyncClient()
