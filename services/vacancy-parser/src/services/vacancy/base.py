from abc import ABC, abstractmethod

from common.shared.services.base import BaseUOWService
from database.models import Vacancy
from repositories import VacancyRepository
from schemas.vacancy import VacancyCreate, VacancyRead
from unitofwork import UnitOfWork


__all__ = ["BaseVacancyService"]


class BaseVacancyService(BaseUOWService[UnitOfWork], ABC):
    _read_schema: type[VacancyRead] = VacancyRead
    _create_schema: type[VacancyCreate] = VacancyCreate
    _repo: VacancyRepository[Vacancy]

    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)
        self._repo = self._get_repo()

    @abstractmethod
    def _get_repo(self) -> VacancyRepository[Vacancy]:
        pass
