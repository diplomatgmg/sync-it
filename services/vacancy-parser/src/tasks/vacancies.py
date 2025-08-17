import asyncio
from datetime import timedelta

from celery_app import app, loop
from common.logger import get_logger
from common.shared.decorators.singleton import singleton
from constants.telegram import channel_links
from parsers import HeadHunterParser, TelegramParser
from unitofwork import UnitOfWork

from services import HeadHunterVacancyService, TelegramVacancyService


__all__ = ["parse_vacancies"]


logger = get_logger(__name__)


@app.task(name="parse_vacancies")
@singleton(timedelta(minutes=30))
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
    async with UnitOfWork() as uow:
        service = TelegramVacancyService(uow)
        parser = TelegramParser(uow, service, channel_links)
        await parser.parse()


async def parse_head_hunter_vacancies() -> None:
    async with UnitOfWork() as uow:
        service = HeadHunterVacancyService(uow)
        parser = HeadHunterParser(uow, service)
        await parser.parse()
