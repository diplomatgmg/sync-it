from celery_app import app
from common.database.engine import get_async_session
from database.services.telegram_vacancy import TelegramVacancyService
from parsers import TelegramParser


__all__ = ["load_telegram_vacancies"]


@app.task(name="load_telegram_vacancies")  # type: ignore[misc]
async def load_telegram_vacancies() -> None:
    async with get_async_session() as session:
        service = TelegramVacancyService(session)
        parser = TelegramParser(service)
        await parser.parse()
