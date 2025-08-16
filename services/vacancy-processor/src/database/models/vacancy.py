from datetime import datetime
from typing import TYPE_CHECKING

from database.models import Base
from database.models.tables import vacancy_grade_table, vacancy_skill_table, vacancy_work_format_table
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


__all__ = ["Vacancy"]


if TYPE_CHECKING:
    from database.models import Grade, Profession, Skill, WorkFormat


class Vacancy(Base):
    __tablename__ = "vacancy"

    id: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(String(32), unique=True)
    link: Mapped[str] = mapped_column(String(256), unique=True)

    company_name: Mapped[str | None] = mapped_column(String(128))
    salary: Mapped[str | None] = mapped_column(String(64))
    workplace_description: Mapped[str | None] = mapped_column(Text)
    responsibilities: Mapped[str | None] = mapped_column(Text)
    requirements: Mapped[str | None] = mapped_column(Text)
    conditions: Mapped[str | None] = mapped_column(Text)

    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    profession_id: Mapped[int | None] = mapped_column(ForeignKey("profession.id", ondelete="CASCADE"))
    profession: Mapped["Profession"] = relationship(back_populates="vacancies")

    grades: Mapped[list["Grade"]] = relationship(secondary=vacancy_grade_table, back_populates="vacancies")
    work_formats: Mapped[list["WorkFormat"]] = relationship(
        secondary=vacancy_work_format_table, back_populates="vacancies"
    )
    skills: Mapped[list["Skill"]] = relationship(secondary=vacancy_skill_table, back_populates="vacancies")
