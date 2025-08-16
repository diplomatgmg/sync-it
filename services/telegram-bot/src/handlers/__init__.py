from aiogram import Dispatcher
from common.logger import get_logger
from handlers import menu, noop, preferences, start, support, vacancies


__all__ = ["register_handler_routers"]


logger = get_logger(__name__)


def register_handler_routers(dp: Dispatcher) -> None:
    logger.info("Registering handlers")

    dp.include_routers(
        noop.router,
        start.router,
        menu.router,
        preferences.router,
        vacancies.router,
        support.router,
    )
