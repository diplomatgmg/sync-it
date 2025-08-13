from collections.abc import Iterable

from common.logger import get_logger
from database.models.vacancy import TelegramVacancy
from parsers.base import BaseParser
from schemas_old import TelegramChannelUrl
from services.http.telegram import fetch_newest_telegram_messages
from services.vacancy import TelegramVacancyService
from utils import generate_fingerprint


__all__ = ["TelegramParser"]


logger = get_logger(__name__)


class TelegramParser(BaseParser):
    service: TelegramVacancyService

    def __init__(self, service: TelegramVacancyService, channel_links: Iterable[TelegramChannelUrl]) -> None:
        super().__init__()
        self.service = service
        self.channel_links = channel_links

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

        # TODO: Создать клиент для работы с Telegram API
        newest_messages = await fetch_newest_telegram_messages(channel_link.channel_username, last_message_id)

        if not newest_messages:
            logger.info("No new messages for channel '%s'", channel_link)
            return

        logger.info("Got %s new messages", len(newest_messages))

        vacancies = []
        for message in newest_messages:
            fingerprint = generate_fingerprint(message.text)
            if fingerprint in self.parsed_fingerprints:
                logger.info("Vacancy with fingerprint '%s' already exists", fingerprint)
                continue

            self.parsed_fingerprints.add(fingerprint)

            duplicate = await self.service.find_duplicate_vacancy_by_fingerprint(fingerprint)
            if duplicate:
                logger.info(
                    "Found duplicate vacancy with similarity %s%%. "
                    "New vacancy link: %s/%s, "
                    "Existing vacancy link: %s, ",
                    await self.service.get_similarity_score(fingerprint, duplicate.fingerprint),
                    channel_link,
                    message.id,
                    duplicate.link,
                )
                continue

            vacancy = await self.service.prepare_instance(
                fingerprint=fingerprint,
                link=f"{channel_link}/{message.id}",
                channel_username=channel_link.channel_username,
                message_id=message.id,
                message_datetime=message.datetime,
                message_text=message.text,
            )
            vacancies.append(vacancy)

            if len(vacancies) >= self.BATCH_SIZE:
                logger.info("Saving batch of %d vacancies...", len(vacancies))
                new_vacancies = await self._get_new_vacancies(vacancies)
                await self.save_vacancies(new_vacancies)
                vacancies.clear()

        if vacancies:
            new_vacancies = await self._get_new_vacancies(vacancies)
            await self.save_vacancies(new_vacancies)

    async def _get_new_vacancies(self, vacancies: list[TelegramVacancy]) -> list[TelegramVacancy]:
        vacancy_hashes = [v.hash for v in vacancies]
        existing_hashes = await self.service.get_existing_hashes(vacancy_hashes)

        return [v for v in vacancies if v.hash not in existing_hashes]
