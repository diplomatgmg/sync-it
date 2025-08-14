from common.shared.unitofwork import BaseUnitOfWork
from database.models import Vacancy
from repositories import HeadHunterVacancyRepository, TelegramVacancyRepository, VacancyRepository


__all__ = ["UnitOfWork"]


class UnitOfWork(BaseUnitOfWork):
    """Конкретная реализация UoW для SQLAlchemy."""

    vacancies: VacancyRepository[Vacancy]
    tg_vacancies: TelegramVacancyRepository
    hh_vacancies: HeadHunterVacancyRepository

    def init_repositories(self) -> None:
        self.vacancies = VacancyRepository(self._session)
        self.tg_vacancies = TelegramVacancyRepository(self._session)
        self.hh_vacancies = HeadHunterVacancyRepository(self._session)
