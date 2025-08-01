from commands import get_bot_commands
from common.logger import get_logger
from core.loader import bot, dp
from handlers import register_handler_routers
from middlewares import register_middlewares
import uvloop


__all__ = ()


logger = get_logger(__name__)


async def on_startup() -> None:
    register_handler_routers(dp)
    register_middlewares(dp)

    await bot.set_my_commands(get_bot_commands())


async def main() -> None:
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
