from common.logger import get_logger
from database.models.enums import WorkFormatEnum
from schemas.work_format import WorkFormatCreate
from unitofwork import UnitOfWork

from services import WorkFormatService


__all__ = ["seed_work_formats"]


logger = get_logger(__name__)


async def seed_work_formats() -> None:
    logger.debug("Start seeding work formats")

    async with UnitOfWork() as uow:
        service = WorkFormatService(uow)
        existing_work_formats = await service.get_work_formats()
        existing_work_format_names = [work_format.name for work_format in existing_work_formats]

        for enum_work_format in WorkFormatEnum:
            if enum_work_format not in existing_work_format_names:
                work_format = WorkFormatCreate(name=enum_work_format)
                await service.add_work_format(work_format)

        await uow.commit()

    logger.info("Work formats seeded")
