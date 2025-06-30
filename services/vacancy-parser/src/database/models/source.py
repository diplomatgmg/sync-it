from database.models import Base
from database.models.enums import SourceEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


__all__ = ["Source"]


class Source(Base):
    __tablename__ = "source"
    _enums = (("name", SourceEnum),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
