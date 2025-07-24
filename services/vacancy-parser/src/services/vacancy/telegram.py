from collections.abc import Sequence

from database.models.vacancy import TelegramVacancy
from repositories.vacancy import TelegramVacancyRepository
from schemas import TelegramChannelUrl
from services.vacancy import BaseVacancyService


__all__ = ["TelegramVacancyService"]


class TelegramVacancyService(BaseVacancyService):
    repo: TelegramVacancyRepository

    def __init__(self, telegram_vacancy_repo: TelegramVacancyRepository) -> None:
        self.repo = telegram_vacancy_repo

    async def get_last_message_id(self, link: TelegramChannelUrl) -> int | None:
        return await self.repo.get_last_message_id(link)

    async def find_duplicate_by_fingerprint(self, fingerprint: str) -> TelegramVacancy | None: ...

    async def prepare_instance(
        self, fingerprint: str, link: str, channel_username: str, message_id: int, data: str
    ) -> TelegramVacancy:
        return await self.repo.prepare_instance(
            fingerprint=fingerprint,
            link=link,
            channel_username=channel_username,
            message_id=message_id,
            data=data,
        )

    async def bulk_create(self, vacancies: Sequence[TelegramVacancy]) -> int:
        return await self.repo.bulk_create(vacancies)
