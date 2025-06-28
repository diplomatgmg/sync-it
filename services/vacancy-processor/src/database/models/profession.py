from database.models import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Profession(Base):
    __tablename__ = "profession"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
