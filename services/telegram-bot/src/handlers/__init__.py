from aiogram import Dispatcher
from common.logger import get_logger
from handlers import noop, start, support, update_preferences, vacancies


__all__ = ["register_handler_routers"]


logger = get_logger(__name__)


def register_handler_routers(dp: Dispatcher) -> None:
    logger.info("Registering handlers")

    dp.include_routers(
        vacancies.router,
        update_preferences.router,
        start.router,
        support.router,
        noop.router,
    )
