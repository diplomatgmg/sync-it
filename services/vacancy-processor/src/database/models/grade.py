from database.models import Base
from database.models.enums import GradeEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


__all__ = ["Grade"]


class Grade(Base):
    __tablename__ = "grade"
    _enums = (("name", GradeEnum),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
