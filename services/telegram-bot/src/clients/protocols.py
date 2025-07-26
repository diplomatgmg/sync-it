from typing import Any, Protocol


__all__ = ["SupportsGetAll"]


class SupportsGetAll(Protocol):
    async def get_all(self) -> list[Any]: ...
