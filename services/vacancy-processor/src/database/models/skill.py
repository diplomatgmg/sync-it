from typing import TYPE_CHECKING

from database.models import Base
from database.models.tables import vacancy_skill_table
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


__all__ = [
    "Skill",
    "SkillCategory",
]


if TYPE_CHECKING:
    from database.models import Vacancy


class SkillCategory(Base):
    __tablename__ = "skill_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)

    skills: Mapped[list["Skill"]] = relationship(back_populates="category")


class Skill(Base):
    __tablename__ = "skill"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)

    category_id: Mapped[int] = mapped_column(ForeignKey("skill_category.id", ondelete="CASCADE"))
    category: Mapped["SkillCategory"] = relationship(back_populates="skills")

    vacancies: Mapped[list["Vacancy"]] = relationship(
        secondary=vacancy_skill_table, back_populates="skills", passive_deletes=True
    )
