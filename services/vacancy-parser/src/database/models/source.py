from database.models import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


__all__ = ["Source"]


class Source(Base):
    __tablename__ = "source"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
