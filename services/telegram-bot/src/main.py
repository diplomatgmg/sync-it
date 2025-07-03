from core.loader import bot, dp
from handlers import register_handler_routers
import uvloop


__all__ = ()


def on_startup() -> None:
    register_handler_routers(dp)


async def main() -> None:
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
