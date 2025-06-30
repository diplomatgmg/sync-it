from database.models import Source
from database.models.enums import SourceEnum
from database.models.vacancy import TelegramVacancy
from database.services.vacancy import VacancyService
from schemas import TelegramChannelUrl
from sqlalchemy import func, select
from utils import required_attrs


__all__ = ["TelegramVacancyService"]


class TelegramVacancyService(VacancyService):
    source = SourceEnum.TELEGRAM
    model = TelegramVacancy

    @required_attrs("model", "source")
    async def get_last_message_id(self, link: TelegramChannelUrl) -> int | None:
        """Получить последний message_id для заданного Telegram канала."""
        source_id = await self.get_source_id()

        smtp = (
            select(func.max(self.model.message_id))
            .join(Source, self.model.source_id == Source.id)
            .where((self.model.source_id == source_id) & (self.model.channel_username == link.channel_username))
        )
        result = await self.session.execute(smtp)
        return result.scalar_one_or_none()
