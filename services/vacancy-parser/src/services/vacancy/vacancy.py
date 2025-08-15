from repositories import VacancyRepository
from schemas.vacancy import VacancyCreate, VacancyRead

from services import AbstractVacancyService


__all__ = ["VacancyService"]


class VacancyService(AbstractVacancyService[VacancyRead, VacancyCreate, VacancyRepository]):
    _read_schema = VacancyRead
    _create_schema = VacancyCreate
    _repo: "VacancyRepository"

    def _get_repo(self) -> "VacancyRepository":
        return self._uow.vacancies
