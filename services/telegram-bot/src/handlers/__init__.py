from aiogram import Dispatcher
from common.logger import get_logger
from handlers import start


logger = get_logger(__name__)


def register_handler_routers(dp: Dispatcher) -> None:
    logger.info("Registering handlers")

    dp.include_routers(
        start.router,
    )
