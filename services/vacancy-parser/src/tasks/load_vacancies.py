from celery_app import app, loop
from common.database.engine import get_async_session
from constants.telegram import channel_links
from database.services.vacancy import TelegramVacancyService
from parsers import TelegramParser


__all__ = ["load_telegram_vacancies"]


@app.task(name="load_vacancies")  # type: ignore[misc]
def load_vacancies() -> None:
    loop.run_until_complete(load_telegram_vacancies())


async def load_telegram_vacancies() -> None:
    async with get_async_session() as session:
        service = TelegramVacancyService(session)
        parser = TelegramParser(service, channel_links)
        await parser.parse()
