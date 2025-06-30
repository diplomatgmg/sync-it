from typing import TYPE_CHECKING

from database.models import Base
from database.models.enums import WorkFormatEnum
from database.models.tables import vacancy_work_format_table
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


__all__ = ["WorkFormat"]


if TYPE_CHECKING:
    from database.models import Vacancy


class WorkFormat(Base):
    __tablename__ = "work_format"
    _enums = (("name", WorkFormatEnum),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)

    vacancies: Mapped[list["Vacancy"]] = relationship(
        secondary=vacancy_work_format_table, back_populates="work_formats", passive_deletes=True
    )
