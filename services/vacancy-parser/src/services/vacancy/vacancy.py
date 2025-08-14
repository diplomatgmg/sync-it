from typing import TYPE_CHECKING

from schemas.vacancy import VacancyCreate, VacancyRead

from services import AbstractVacancyService


__all__ = ["VacancyService"]


if TYPE_CHECKING:
    from repositories import VacancyRepository


class VacancyService[
    VacancyReadType: VacancyRead = VacancyRead,
    VacancyCreateType: VacancyCreate = VacancyCreate,
    VacancyRepositoryType: VacancyRepository = VacancyRepository,
](AbstractVacancyService[VacancyReadType, VacancyCreateType, VacancyRepositoryType]):
    _read_schema: type[VacancyReadType] = VacancyRead  # type: ignore[assignment]
    _create_schema: type[VacancyCreateType] = VacancyCreate  # type: ignore[assignment]
    _repo: "VacancyRepository"  # type: ignore[assignment]

    def _get_repo(self) -> "VacancyRepository":  # type: ignore[override]
        return self._uow.vacancies
