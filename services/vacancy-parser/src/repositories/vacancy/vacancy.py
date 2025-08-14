from database.models import Vacancy
from repositories import AbstractVacancyRepository


__all__ = ["VacancyRepository"]


class VacancyRepository[VacancyType: Vacancy = Vacancy](AbstractVacancyRepository[VacancyType]):
    """Репозиторий для работы с моделями вакансий."""

    _model = Vacancy  # type: ignore[assignment]
