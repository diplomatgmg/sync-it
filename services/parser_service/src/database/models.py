from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

from database.utils import get_service_schema


class Base(DeclarativeBase, AsyncAttrs):
    __table_args__ = {"schema": get_service_schema("parser")}
