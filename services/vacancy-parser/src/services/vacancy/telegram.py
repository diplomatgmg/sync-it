from database.models.vacancy import TelegramVacancy
from parsers.schemas import TelegramChannelUrl
from schemas.vacancy import TelegramVacancyCreate, TelegramVacancyRead
from services.vacancy import BaseVacancyService


__all__ = ["TelegramVacancyService"]


class TelegramVacancyService(BaseVacancyService):
    """Сервис для бизнес-логики, связанной с вакансиями из Телеграма."""

    vacancy_create_schema: TelegramVacancyCreate
    vacancy_read_schema: TelegramVacancyRead

    async def get_last_message_id(self, link: TelegramChannelUrl) -> int | None:
        return await self._uow.tg_vacancies.get_last_message_id(link)

    async def add_vacancy(self, vacancy: TelegramVacancyCreate) -> TelegramVacancyRead:
        source_id = await self._uow.vacancies.get_source_id()

        vacancy_model = TelegramVacancy(
            source_id=source_id,
            **vacancy.model_dump(),
        )
        created_vacancy = await self._uow.tg_vacancies.add(vacancy_model)

        return self.vacancy_read_schema.model_validate(created_vacancy)
