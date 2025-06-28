from database.models import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


__all__ = ["WorkFormat"]


class WorkFormat(Base):
    __tablename__ = "work_format"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
