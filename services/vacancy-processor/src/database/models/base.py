from typing import Any

from core.config import service_config
from database.models.enums import BaseStrEnum
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


__all__ = ["Base"]


metadata_obj = MetaData(schema=service_config.db_schema)


class Base(DeclarativeBase, AsyncAttrs):
    metadata = metadata_obj
    # Для проверки, что поле модели соответствует значению в enum
    _enums: tuple[tuple[str, type[BaseStrEnum]], ...] = ()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__()

        for k, v in kwargs.items():
            setattr(self, k, v)

        self._validate_enum_labels()

    def _validate_enum_labels(self) -> None:
        """Проверяет, поля модели соответствуют значению в enum."""
        for field_name, enum_type in self._enums:
            value = getattr(self, field_name)
            if value is None:
                raise ValueError(f'Field "{field_name}" not exist in model "{self.__class__.__name__}"')

            enum_value = enum_type.get_safe(value)
            if enum_value is None:
                raise TypeError(f'Invalid value "{value}" for enum "{enum_type.__name__}"')
