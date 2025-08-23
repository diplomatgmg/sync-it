from enum import StrEnum
from typing import Any, Self


__all__ = ["BaseAliasEnum"]


class BaseAliasEnum(StrEnum):
    aliases: tuple[str, ...]  # type: ignore[misc]
    __validate_ordering__: bool
    __ignore_patterns__: tuple[str, ...]

    def __new__(cls, normalized: str, aliases: tuple[str, ...] = ()) -> Self:
        obj = str.__new__(cls, normalized)
        obj._value_ = normalized
        obj.aliases = (normalized.lower(), *(a for a in aliases))  # type: ignore[misc]
        return obj

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Проверяем, что у наследников есть UNKNOWN"""
        super().__init_subclass__(**kwargs)
        if "UNKNOWN" not in cls.__members__:
            raise ValueError(f"{cls.__name__} must define UNKNOWN member")

        if getattr(cls, "__validate_ordering__", False):
            cls._check_members_order()

        cls._validate_register()

    @classmethod
    def get_safe(cls, label: str) -> Self | None:
        """Возвращает элемент Enum по строковому значению или алиасу."""
        for member in cls:
            if label.lower() in member.aliases:
                return member

        return None

    @classmethod
    def _check_members_order(cls) -> None:
        """Проверяет, что элементы перечисления отсортированы по значению."""
        original_members = [item[0] for item in cls.__members__.items() if item[1] != cls.UNKNOWN]  # type: ignore[attr-defined]
        sorted_members = sorted(original_members, key=lambda item: item.casefold())

        if original_members != sorted_members:
            # Находим первый элемент, который нарушает порядок
            for i, (name_original, name_sorted) in enumerate(zip(original_members, sorted_members, strict=True)):
                if name_original != name_sorted:
                    raise ValueError(
                        f"Ordering error in {cls.__name__}: member '{name_original}' is out of order."
                        f"\nExpected order: ... {sorted_members[i - 1]}, {sorted_members[i]}, {sorted_members[i + 1]} ..."  # noqa: E501
                        f"\nActual order: ... {original_members[i - 1]}, {original_members[i]}, {original_members[i + 1]} ..."  # noqa: E501
                    )

    @classmethod
    def _validate_register(cls) -> None:
        for key, value in cls.__members__.items():
            if not key.isupper():
                raise ValueError(f"{cls.__name__} has non-uppercase member: {key}.")
            if not all(a == a.lower() for a in value.aliases):
                aliases = value.aliases[1:]  # Пропускаем оригинальный алиас (значение)
                raise ValueError(f"{cls.__name__} has non-lowercase alias: {aliases}.")
