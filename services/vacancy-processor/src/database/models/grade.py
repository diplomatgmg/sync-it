from typing import TYPE_CHECKING

from database.models import Base
from database.models.enums import GradeEnum
from database.models.tables import vacancy_grade_table
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


__all__ = ["Grade"]


if TYPE_CHECKING:
    from database.models import Vacancy


class Grade(Base):
    __tablename__ = "grade"
    _enums = (("name", GradeEnum),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)

    vacancies: Mapped[list["Vacancy"]] = relationship(
        secondary=vacancy_grade_table, back_populates="grades", passive_deletes=True
    )
