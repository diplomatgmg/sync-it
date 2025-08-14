from typing import TYPE_CHECKING

from database.models import HeadHunterVacancy
from schemas.vacancy import HeadHunterVacancyCreate, HeadHunterVacancyRead

from services import VacancyService


if TYPE_CHECKING:
    from repositories import HeadHunterVacancyRepository


__all__ = ["HeadHunterVacancyService"]


class HeadHunterVacancyService(VacancyService):
    """Сервис для бизнес-логики, связанной с вакансиями из HeadHunter."""

    _read_schema = HeadHunterVacancyRead
    _create_schema = HeadHunterVacancyCreate
    _repo: "HeadHunterVacancyRepository"

    def _get_repo(self) -> "HeadHunterVacancyRepository":
        return self._uow.hh_vacancies

    async def get_vacancy_by_id(self, vacancy_id: int) -> HeadHunterVacancyRead | None:
        vacancy = await self._repo.get_vacancy_by_id(vacancy_id)

        return self._read_schema.model_validate(vacancy) if vacancy else None

    async def add_vacancy(self, vacancy: HeadHunterVacancyCreate) -> HeadHunterVacancyRead:
        vacancy_model = HeadHunterVacancy(**vacancy.model_dump())
        created_vacancy = await self._repo.add(vacancy_model)

        return self._read_schema.model_validate(created_vacancy)
