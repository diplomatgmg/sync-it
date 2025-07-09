from types import TracebackType
from typing import Self

from httpx import URL, AsyncClient


__all__ = ["BaseClient"]


class BaseClient:
    url: URL

    def __init__(self) -> None:
        self._internal_client: AsyncClient | None = None

    async def __aenter__(self) -> Self:
        self._internal_client = AsyncClient()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._internal_client:
            await self._internal_client.aclose()

    @property
    def client(self) -> AsyncClient:
        if self._internal_client is None:
            raise RuntimeError(f"Client is not initialized. Use 'async with {self.__class__.__name__}()'.")
        return self._internal_client
