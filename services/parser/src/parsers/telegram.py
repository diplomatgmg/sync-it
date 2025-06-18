
from core.config import parser_config
from database.models import TelegramVacancy
from database.services.telegram_vacancy import TelegramVacancyService
from parsers.base import BaseParser

from libs.database.engine import get_async_session
from libs.logger import get_logger


__all__ = ["TelegramParser"]

from services.telegram_messages import get_newest_telegram_messages

logger = get_logger(__name__)


class TelegramParser(BaseParser):
    def __init__(self) -> None:
        super().__init__()
        self.channel_links = parser_config.telegram_channel_links

    async def parse(self) -> None:
        logger.info("Starting Telegram parser")

        for channel_link in self.channel_links:
            logger.info("Start parsing channel '%s'", channel_link)
            async with get_async_session() as session:
                tg_service = TelegramVacancyService(session)
                last_parsed_message_id = await tg_service.get_last_message_id_by_channel(channel_link)
                newest_messages = await get_newest_telegram_messages(
                    channel_link.channel_username,
                    last_parsed_message_id
                )

                if not newest_messages:
                    logger.info("No new messages")
                    continue

                vacancies = [
                    TelegramVacancy.create(
                        channel_link=channel_link,
                        message_id=message.message_id,
                        message=message.text
                    )
                    for message in newest_messages
                ]
                await self.save_vacancies(vacancies)

    @staticmethod
    async def save_vacancies(vacancies: list[TelegramVacancy]) -> None:
        logger.debug("Start saving %s vacancies", len(vacancies))

        async with get_async_session() as session:
            tg_service = TelegramVacancyService(session)

            vacancy_hashes = [v.hash for v in vacancies]
            existing_hashes = await tg_service.get_existing_hashes(vacancy_hashes)

            vacancies_to_save = [v for v in vacancies if v.hash not in existing_hashes]
            logger.info("Saving %s vacancies", len(vacancies_to_save))

            saved_count = await tg_service.bulk_add_vacancies(vacancies_to_save)
            logger.info("Saved %s vacancies", saved_count)
