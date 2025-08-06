import asyncio

from celery_app import app, loop
from common.database.engine import get_async_session
from common.logger import get_logger
from constants.telegram import channel_links
from parsers import HeadHunterParser, TelegramParser
from repositories.vacancy import HeadHunterVacancyRepository, TelegramVacancyRepository
from services.vacancy import HeadHunterVacancyService, TelegramVacancyService


__all__ = ["parse_vacancies"]


logger = get_logger(__name__)


@app.task(name="parse_vacancies")
def parse_vacancies() -> None:
    """Основная задача Celery для запуска всех парсеров."""
    loop.run_until_complete(run_all_parsers())


async def run_all_parsers() -> None:
    """Запускает все парсеры параллельно и обрабатывает результаты."""
    logger.info("Run all parsers")

    results = await asyncio.gather(
        parse_telegram_vacancies(),
        parse_head_hunter_vacancies(),
        return_exceptions=True,
    )

    for result in results:
        if isinstance(result, Exception):
            logger.error("Error running parser", exc_info=result)


async def parse_telegram_vacancies() -> None:
    async with get_async_session() as session:
        repo = TelegramVacancyRepository(session)
        service = TelegramVacancyService(repo)
        parser = TelegramParser(service, channel_links)
        await parser.parse()
        await session.commit()


async def parse_head_hunter_vacancies() -> None:
    async with get_async_session() as session:
        repo = HeadHunterVacancyRepository(session)
        service = HeadHunterVacancyService(repo)
        parser = HeadHunterParser(service)
        await parser.parse()
        await session.commit()
