from database.models import Vacancy
from repositories import AbstractVacancyRepository


__all__ = ["VacancyRepository"]


class VacancyRepository(AbstractVacancyRepository[Vacancy]):
    """Репозиторий для работы с моделями вакансий."""

    _model = Vacancy
