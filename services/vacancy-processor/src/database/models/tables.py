from database.models import Base
from sqlalchemy import Column, ForeignKey, Table


__all__ = [
    "vacancy_grade_table",
    "vacancy_skill_table",
    "vacancy_work_format_table",
]


vacancy_grade_table: Table = Table(
    "vacancy_grade",
    Base.metadata,
    Column("vacancy_id", ForeignKey("vacancy.id", ondelete="CASCADE"), primary_key=True),
    Column("grade_id", ForeignKey("grade.id", ondelete="RESTRICT"), primary_key=True),
)

vacancy_skill_table: Table = Table(
    "vacancy_skill",
    Base.metadata,
    Column("vacancy_id", ForeignKey("vacancy.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", ForeignKey("skill.id", ondelete="RESTRICT"), primary_key=True),
)


vacancy_work_format_table: Table = Table(
    "vacancy_work_format",
    Base.metadata,
    Column("vacancy_id", ForeignKey("vacancy.id", ondelete="CASCADE"), primary_key=True),
    Column("work_format_id", ForeignKey("work_format.id", ondelete="RESTRICT"), primary_key=True),
)
