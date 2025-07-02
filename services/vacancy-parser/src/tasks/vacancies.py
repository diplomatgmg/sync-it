from celery_app import app, loop
from common.database.engine import get_async_session
from constants.telegram import channel_links
from database.services.vacancy import TelegramVacancyService
from services.parsers import TelegramParserService


__all__ = ["parse_vacancies"]


@app.task(name="parse_vacancies")  # type: ignore[misc]
def parse_vacancies() -> None:
    loop.run_until_complete(parse_telegram_vacancies())


async def parse_telegram_vacancies() -> None:
    async with get_async_session() as session:
        service = TelegramVacancyService(session)
        parser = TelegramParserService(service, channel_links)
        await parser.parse()
