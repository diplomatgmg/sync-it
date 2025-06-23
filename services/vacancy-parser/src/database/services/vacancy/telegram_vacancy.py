from database.models.vacancy import TelegramVacancy
from database.models.vacancy.enums import VacancySource
from database.services.vacancy import VacancyService
from schemas import TelegramChannelUrl
from sqlalchemy import func, select
from utils import required_attrs


__all__ = ["TelegramVacancyService"]


class TelegramVacancyService(VacancyService):
    source = VacancySource.TELEGRAM
    model = TelegramVacancy

    @required_attrs("model", "source")
    async def get_last_message_id(self, link: TelegramChannelUrl) -> int | None:
        """Получить последний message_id для заданного Telegram канала."""
        smtp = select(func.max(self.model.message_id)).where(
            (self.model.source == self.source) & (self.model.channel_username == link.channel_username)
        )
        result = await self.session.execute(smtp)
        return result.scalar_one_or_none()
