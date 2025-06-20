from common.logger import get_logger
from core.config import parser_config
from database.models.vacancy import TelegramVacancy
from database.services.telegram_vacancy import TelegramVacancyService
from parsers.base import BaseParser
from schemas import TelegramChannelUrl
from services.telegram_messages import get_newest_telegram_messages


__all__ = ["TelegramParser"]


logger = get_logger(__name__)


class TelegramParser(BaseParser):
    def __init__(self, service: TelegramVacancyService) -> None:
        super().__init__(service)
        self.channel_links = parser_config.telegram_channel_links

    async def parse(self) -> None:
        logger.info("Starting Telegram parser")

        for channel_link in self.channel_links:
            try:
                await self._process_channel(channel_link)
            except Exception as e:
                logger.exception("Error processing channel '%s'", channel_link, exc_info=e)

    async def _process_channel(self, channel_link: TelegramChannelUrl) -> None:
        logger.info("Start parsing channel '%s'", channel_link)

        last_message_id = await self.service.get_last_message_id(channel_link)
        logger.info("Last message id for channel '%s' is %s", channel_link, last_message_id)

        newest_messages = await get_newest_telegram_messages(channel_link.channel_username, last_message_id)

        if not newest_messages:
            logger.info("No new messages for channel '%s'", channel_link)
            return

        logger.info("Got %s new messages", len(newest_messages))

        vacancies = [
            TelegramVacancy.create(
                link=f"{channel_link}/{message.message_id}",
                channel_username=channel_link.channel_username,
                message_id=message.message_id,
                data=message.text,
            )
            for message in newest_messages
        ]

        await self.save_vacancies(vacancies)

    async def save_vacancies(self, vacancies: list[TelegramVacancy]) -> None:
        logger.debug("Checking %s vacancies for uniqueness", len(vacancies))

        vacancy_hashes = [v.hash for v in vacancies]
        existing_hashes = await self.service.get_existing_hashes(vacancy_hashes)

        new_vacancies = [v for v in vacancies if v.hash not in existing_hashes]

        if not new_vacancies:
            logger.info("No new vacancies to save")
            return

        saved_count = await self.service.bulk_add_vacancies(new_vacancies)
        logger.info("Saved %s new vacancies", saved_count)
