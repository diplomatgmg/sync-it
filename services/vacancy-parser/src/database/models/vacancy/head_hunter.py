from database.models.enums import SourceEnum
from database.models.vacancy import BaseVacancy
from sqlalchemy.orm import Mapped, mapped_column


__all__ = ["HeadHunterVacancy"]


class HeadHunterVacancy(BaseVacancy):
    __tablename__ = "head_hunter_vacancy"

    vacancy_id: Mapped[int] = mapped_column(nullable=False)

    def get_source(self) -> SourceEnum:  # noqa: PLR6301
        return SourceEnum.HEAD_HUNTER
