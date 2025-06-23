from collections.abc import Awaitable, Callable
from functools import wraps
import hashlib
from typing import Any, ParamSpec, TypeVar, cast


__all__ = [
    "generate_hash",
    "required_attrs",
]


def generate_hash(value: str, algorithm: str = "md5") -> str:
    """Генерирует хеш на основе переданного значения и алгоритма."""
    hasher = hashlib.new(algorithm)
    hasher.update(value.encode("utf-8"))

    return hasher.hexdigest()


_P = ParamSpec("_P")
_R = TypeVar("_R")


def required_attrs(*attrs: str) -> Callable[[Callable[_P, Awaitable[_R]]], Callable[_P, Awaitable[_R]]]:
    """Декоратор для проверки наличия обязательных атрибутов в экземпляре класса перед вызовом метода."""

    def decorator(func: Callable[_P, Awaitable[_R]]) -> Callable[_P, Awaitable[_R]]:
        @wraps(func)
        async def wrapper(self: Any, *args: _P.args, **kwargs: _P.kwargs) -> _R:
            missing = [attr for attr in attrs if not hasattr(self, attr)]
            if missing:
                raise AttributeError(f"Missing attributes for {func.__name__}: {', '.join(missing)}")
            return await func(self, *args, **kwargs)

        return cast("Callable[_P, Awaitable[_R]]", wrapper)

    return decorator
