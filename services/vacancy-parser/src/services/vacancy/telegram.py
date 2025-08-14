from database.models import TelegramVacancy
from parsers.schemas import TelegramChannelUrl
from schemas.vacancy import TelegramVacancyCreate, TelegramVacancyRead

from services import VacancyService


__all__ = ["TelegramVacancyService"]


class TelegramVacancyService(VacancyService[TelegramVacancyRead, TelegramVacancyCreate]):
    """Сервис для бизнес-логики, связанной с вакансиями из Телеграма."""

    _read_schema = TelegramVacancyRead
    _create_schema = TelegramVacancyCreate

    async def get_last_message_id(self, link: TelegramChannelUrl) -> int | None:
        return await self._uow.tg_vacancies.get_last_message_id(link)

    async def add_vacancy(self, vacancy: TelegramVacancyCreate) -> TelegramVacancyRead:
        vacancy_model = TelegramVacancy(**vacancy.model_dump())
        created_vacancy = await self._uow.tg_vacancies.add(vacancy_model)

        return self._read_schema.model_validate(created_vacancy)
