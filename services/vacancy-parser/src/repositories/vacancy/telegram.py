from database.models import Source
from database.models.enums import SourceEnum
from database.models.vacancy import TelegramVacancy
from parsers.schemas import TelegramChannelUrl
from repositories.vacancy.vacancy import VacancyRepository
from sqlalchemy import func, select


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
