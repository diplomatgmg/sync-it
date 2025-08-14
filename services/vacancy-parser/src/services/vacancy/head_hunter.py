from database.models import HeadHunterVacancy
from schemas.vacancy import HeadHunterVacancyCreate, HeadHunterVacancyRead

from services import BaseVacancyService


__all__ = ["HeadHunterVacancyService"]


class HeadHunterVacancyService(BaseVacancyService):
    """Сервис для бизнес-логики, связанной с вакансиями из HeadHunter."""

    vacancy_create_schema: HeadHunterVacancyCreate
    vacancy_read_schema: HeadHunterVacancyRead

    async def get_vacancy_by_id(self, vacancy_id: int) -> HeadHunterVacancyRead | None:
        vacancy = await self._uow.hh_vacancies.get_vacancy_by_id(vacancy_id)

        return self.vacancy_read_schema.model_validate(vacancy) if vacancy else None

    async def add_vacancy(self, vacancy: HeadHunterVacancyCreate) -> HeadHunterVacancyRead:
        vacancy_model = HeadHunterVacancy(**vacancy.model_dump())
        created_vacancy = await self._uow.hh_vacancies.add(vacancy_model)

        return self.vacancy_read_schema.model_validate(created_vacancy)
