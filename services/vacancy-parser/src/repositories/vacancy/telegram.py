from datetime import datetime

from database.models import Source
from database.models.enums import SourceEnum
from database.models.vacancy import TelegramVacancy
from repositories.vacancy.vacancy import VacancyRepository
from schemas import TelegramChannelUrl
from sqlalchemy import func, select
from utils import generate_hash


__all__ = ["TelegramVacancyRepository"]


class TelegramVacancyRepository(VacancyRepository):
    source = SourceEnum.TELEGRAM
    model = TelegramVacancy

    async def get_last_message_id(self, link: TelegramChannelUrl) -> int | None:
        """Получить последний message_id для заданного Telegram канала."""
        source_id = await self.get_source_id()

        smtp = (
            select(func.max(self.model.message_id))
            .join(Source, self.model.source_id == Source.id)
            .where((self.model.source_id == source_id) & (self.model.channel_username == link.channel_username))
        )
        result = await self._session.execute(smtp)
        return result.scalar_one_or_none()

    async def prepare_instance(
        self,
        *,
        fingerprint: str,
        link: str,
        channel_username: str,
        message_id: int,
        published_at: datetime,
        data: str,
    ) -> TelegramVacancy:
        """Создает экземпляр TelegramVacancy, сохраняет его и возвращает."""
        hash_value = generate_hash(f"{link}:{message_id}")
        source_id = await self.get_source_id()

        return self.model(
            hash=hash_value,
            source_id=source_id,
            fingerprint=fingerprint,
            link=link,
            channel_username=channel_username,
            message_id=message_id,
            published_at=published_at,
            data=data,
        )
