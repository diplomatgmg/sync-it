from database.models import Base
from database.models.enums import SkillCategoryEnum, SkillEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


__all__ = [
    "Skill",
    "SkillCategory",
]


class SkillCategory(Base):
    __tablename__ = "skill_category"
    _enums = (("name", SkillCategoryEnum),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)

    skills: Mapped[list["Skill"]] = relationship(back_populates="category")


class Skill(Base):
    __tablename__ = "skill"
    _enums = (("name", SkillEnum),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)

    category_id: Mapped[int | None] = mapped_column(ForeignKey("skill_category.id", ondelete="CASCADE"))
    category: Mapped["SkillCategory"] = relationship(back_populates="skills")
