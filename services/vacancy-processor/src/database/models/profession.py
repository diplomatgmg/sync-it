from typing import TYPE_CHECKING

from database.models import Base
from database.models.enums import ProfessionEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


__all__ = ["Profession"]


if TYPE_CHECKING:
    from database.models import Vacancy


class Profession(Base):
    __tablename__ = "profession"
    _enums = (("name", ProfessionEnum),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)

    vacancies: Mapped[list["Vacancy"]] = relationship(back_populates="profession")
