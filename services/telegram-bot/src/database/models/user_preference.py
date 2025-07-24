from typing import TYPE_CHECKING

from database.models import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


__all__ = ["UserPreference"]


if TYPE_CHECKING:
    from database.models import User


class UserPreference(Base):
    __tablename__ = "user_preference"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # ex.: grade, profession, work_format
    category_code: Mapped[str] = mapped_column(String(16), nullable=False, index=True)

    item_id: Mapped[int] = mapped_column(nullable=False)
    item_name: Mapped[str] = mapped_column(String(32), nullable=False)

    user: Mapped["User"] = relationship(back_populates="preferences")
