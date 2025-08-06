from datetime import datetime

from database.models.vacancy import TelegramVacancy
from repositories.vacancy import TelegramVacancyRepository
from schemas import TelegramChannelUrl
from services.vacancy import BaseVacancyService


__all__ = ["TelegramVacancyService"]


class TelegramVacancyService(BaseVacancyService[TelegramVacancyRepository]):
    """Сервис для бизнес-логики, связанной с вакансиями из Телеграма."""

    async def get_last_message_id(self, link: TelegramChannelUrl) -> int | None:
        return await self._repo.get_last_message_id(link)

    async def find_duplicate_by_fingerprint(self, fingerprint: str) -> TelegramVacancy | None: ...

    async def prepare_instance(
        self,
        fingerprint: str,
        link: str,
        channel_username: str,
        message_id: int,
        message_datetime: datetime,
        message_text: str,
    ) -> TelegramVacancy:
        return await self._repo.prepare_instance(
            fingerprint=fingerprint,
            link=link,
            channel_username=channel_username,
            message_id=message_id,
            published_at=message_datetime,
            data=message_text,
        )
