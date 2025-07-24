from core import service_config
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


__all__ = ["Base"]


metadata_obj = MetaData(schema=service_config.db_schema)


class Base(DeclarativeBase, AsyncAttrs):
    metadata = metadata_obj
