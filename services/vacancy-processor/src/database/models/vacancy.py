from typing import TYPE_CHECKING

from database.models import Base
from database.models.tables import vacancy_grade_table, vacancy_skill_table, vacancy_work_format_table
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


__all__ = ["Vacancy"]


if TYPE_CHECKING:
    from database.models import Grade, Profession, Skill, WorkFormat


class Vacancy(Base):
    __tablename__ = "vacancy"

    id: Mapped[int] = mapped_column(primary_key=True)

    hash: Mapped[str] = mapped_column(String(32), unique=True)
    link: Mapped[str] = mapped_column(String(256), unique=True)

    workplace_description: Mapped[str] = mapped_column(Text(), nullable=True)
    responsibilities: Mapped[str] = mapped_column(Text())
    requirements: Mapped[str] = mapped_column(Text())
    conditions: Mapped[str] = mapped_column(Text())

    profession_id: Mapped[int] = mapped_column(ForeignKey("profession.id", ondelete="CASCADE"), nullable=True)
    profession: Mapped["Profession"] = relationship(back_populates="vacancies")

    grades: Mapped[list["Grade"]] = relationship(secondary=vacancy_grade_table, back_populates="vacancies")
    work_formats: Mapped[list["WorkFormat"]] = relationship(
        secondary=vacancy_work_format_table, back_populates="vacancies"
    )
    skills: Mapped[list["Skill"]] = relationship(secondary=vacancy_skill_table, back_populates="vacancies")
