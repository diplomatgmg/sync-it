import asyncio
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import ParamSpec, TypeVar


__all__ = ["limit_concurrency"]


P = ParamSpec("P")
R = TypeVar("R")


def limit_concurrency(limit: int) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """Декоратор, который ограничивает количество одновременных вызовов асинхронной функции."""
    semaphore = asyncio.Semaphore(limit)

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            async with semaphore:
                return await func(*args, **kwargs)

        return wrapper

    return decorator
