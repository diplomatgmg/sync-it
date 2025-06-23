from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


__all__ = ["Base"]


metadata_obj = MetaData(schema="vacancy_processor")


class Base(DeclarativeBase, AsyncAttrs):
    metadata = metadata_obj
