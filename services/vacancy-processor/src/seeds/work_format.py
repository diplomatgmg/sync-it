from common.database.engine import get_async_session
from common.logger import get_logger
from database.models.enums import WorkFormatEnum
from repositories import WorkFormatRepository

from services import WorkFormatService


__all__ = ["seed_work_formats"]


logger = get_logger(__name__)


async def seed_work_formats() -> None:
    logger.debug("Start seeding work formats")

    async with get_async_session() as session:
        repo = WorkFormatRepository(session)
        service = WorkFormatService(repo)
        existing_work_formats = await service.get_work_formats()
        existing_work_format_names = [work_format.name for work_format in existing_work_formats]

        for enum_work_format in WorkFormatEnum:
            if enum_work_format not in existing_work_format_names:
                await service.add_work_format(enum_work_format)

        await session.commit()

    logger.info("Work formats seeded")
