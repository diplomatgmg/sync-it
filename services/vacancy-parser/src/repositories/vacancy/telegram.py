from database.models import TelegramVacancy
from parsers.schemas import TelegramChannelUrl
from repositories import VacancyRepository
from sqlalchemy import func, select


__all__ = ["TelegramVacancyRepository"]


class TelegramVacancyRepository(VacancyRepository[TelegramVacancy]):
    _model = TelegramVacancy

    async def get_last_message_id(self, link: TelegramChannelUrl) -> int | None:
        """Получить последний message_id для заданного Telegram канала."""
        smtp = select(func.max(self._model.message_id)).where(self._model.channel_username == link.channel_username)
        result = await self._session.execute(smtp)
        return result.scalar_one_or_none()

    async def add(self, vacancy: TelegramVacancy) -> TelegramVacancy:
        self._session.add(vacancy)
        await self._session.flush()
        await self._session.refresh(vacancy)

        return vacancy
