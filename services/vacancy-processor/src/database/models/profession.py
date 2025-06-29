from database.models import Base
from database.models.enums import ProfessionEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


__all__ = ["Profession"]


class Profession(Base):
    __tablename__ = "profession"
    _enums = (("name", ProfessionEnum),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
