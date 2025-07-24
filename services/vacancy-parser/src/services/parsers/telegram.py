from collections.abc import Iterable

from common.logger import get_logger
from database.models.vacancy import TelegramVacancy
from schemas import TelegramChannelUrl
from services.http.telegram import fetch_newest_telegram_messages
from services.parsers.base import BaseParser
from services.vacancy import TelegramVacancyService
from utils import generate_fingerprint


__all__ = ["TelegramParserService"]


logger = get_logger(__name__)


class TelegramParserService(BaseParser):
    def __init__(self, service: TelegramVacancyService, channel_links: Iterable[TelegramChannelUrl]) -> None:
        self.service = service
        self.channel_links = channel_links
        # Запоминаем fingerprints, которые получили на основе новых спарсенных вакансий, чтобы избежать конфликта с БД
        self._new_fingerprints: set[str] = set()

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

        newest_messages = await fetch_newest_telegram_messages(channel_link.channel_username, last_message_id)

        if not newest_messages:
            logger.info("No new messages for channel '%s'", channel_link)
            return

        logger.info("Got %s new messages", len(newest_messages))

        vacancies = []
        for message in newest_messages:
            fingerprint = generate_fingerprint(message.text)

            duplicate = await self.service.find_duplicate_vacancy_by_fingerprint(fingerprint)
            if duplicate:
                logger.info(
                    "Found duplicate vacancy with similarity %s%%. "
                    "New vacancy link: %s/%s, "
                    "Existing vacancy link: %s, ",
                    await self.service.get_similarity_score(fingerprint, duplicate.fingerprint),
                    channel_link,
                    message.message_id,
                    duplicate.link,
                )
                continue

            if fingerprint in self._new_fingerprints:
                logger.info("Vacancy with fingerprint '%s' already exists", fingerprint)
                continue

            self._new_fingerprints.add(fingerprint)

            vacancy = await self.service.prepare_instance(
                fingerprint=fingerprint,
                link=f"{channel_link}/{message.message_id}",
                channel_username=channel_link.channel_username,
                message_id=message.message_id,
                data=message.text,
            )
            vacancies.append(vacancy)

        await self.save_vacancies(vacancies)

    async def save_vacancies(self, vacancies: list[TelegramVacancy]) -> None:
        logger.debug("Saving %s vacancies", len(vacancies))

        vacancy_hashes = [v.hash for v in vacancies]
        existing_hashes = await self.service.get_existing_hashes(vacancy_hashes)

        new_vacancies = [v for v in vacancies if v.hash not in existing_hashes]
        if not new_vacancies:
            logger.info("No new vacancies to save")
            return

        saved_count = await self.service.bulk_create(new_vacancies)
        logger.info("Saved %s new vacancies", saved_count)
