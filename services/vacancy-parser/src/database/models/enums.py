from enum import StrEnum
from typing import Self, TypeVar


__all__ = [
    "BaseStrEnum",
    "SourceEnum",
]


T = TypeVar("T", bound="BaseStrEnum")


class BaseStrEnum(StrEnum):
    @classmethod
    def get_safe(cls, label: str) -> Self | None:
        """Возвращает элемент Enum по строковому значению, с игнорированием регистра."""
        for member in cls:
            if member.value.lower() == label.lower():
                return member
        return None


class SourceEnum(BaseStrEnum):
    TELEGRAM = "telegram"
    HH = "hh"
