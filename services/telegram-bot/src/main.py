from clients import GradeClient, ProfessionClient, WorkFormatClient
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
    async with ProfessionClient() as prof_client, GradeClient() as grade_client, WorkFormatClient() as wf_client:
        professions = await prof_client.get_professions()
        grades = await grade_client.get_grades()
        work_formats = await wf_client.get_work_formats()

    logger.info("Professions: %s", professions)
    logger.info("Grades: %s", grades)
    logger.info("Work formats: %s", work_formats)

    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
