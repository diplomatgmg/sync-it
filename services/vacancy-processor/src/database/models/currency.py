from database.models import Base
from database.models.enums import CurrencyEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


__all__ = ["Currency"]


class Currency(Base):
    __tablename__ = "currency"
    _enums = (("value", CurrencyEnum),)

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(32), unique=True)
