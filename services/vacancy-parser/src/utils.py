from collections.abc import Awaitable, Callable
from functools import wraps
import hashlib
import re
from typing import Any, ParamSpec, TypeVar, cast


__all__ = [
    "generate_fingerprint",
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


# Слова, которые часто встречаются в описании вакансии
stop_words = {"и", "с", "в"}


def generate_fingerprint(text: str) -> str:
    """
    Генерирует fingerprint (отпечаток) на основе переданного текста.
    Fingerprint используется для поиска одинаковых вакансий на уровне БД, используя расширение pg_trgm.

    Пример:
    >>> generate_fingerprint("3+ years. Junior/Middle Python developer; (Ex@mp1e c0mpany) #deleted")
    '(exmp1e 3 c0mpany) developer; junior/middle python years.'
    """
    # Удаляем слова, начинающиеся с хештега
    text = re.sub(r"#\w+\s*", "", text)
    # Удаляем URL-адресы
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    # Удаляем лишние символы
    text = re.sub(r"[^а-яa-z0-9/;().\s]", "", text.lower())
    filtered_words = [word for word in text.split() if word not in stop_words]
    sorted_words = sorted(filtered_words)
    return " ".join(sorted_words)
