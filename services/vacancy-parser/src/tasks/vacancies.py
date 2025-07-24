from celery_app import app, loop
from common.database.engine import get_async_session
from constants.telegram import channel_links
from repositories.vacancy import TelegramVacancyRepository
from services.parsers import TelegramParserService
from services.vacancy import TelegramVacancyService


__all__ = ["parse_vacancies"]


@app.task(name="parse_vacancies")  # type: ignore[misc]
def parse_vacancies() -> None:
    loop.run_until_complete(parse_telegram_vacancies())


async def parse_telegram_vacancies() -> None:
    async with get_async_session() as session:
        repo = TelegramVacancyRepository(session)
        service = TelegramVacancyService(repo)
        parser = TelegramParserService(service, channel_links)
        await parser.parse()
