from common.logger import get_logger
from database.models.enums import SourceEnum
from schemas.source import SourceCreate
from services.source import SourceService
from unitofwork import UnitOfWork


__all__ = ["seed_sources"]


logger = get_logger(__name__)


async def seed_sources() -> None:
    logger.debug("Start seeding sources")

    async with UnitOfWork() as uow:
        source_service = SourceService(uow)

        existing_sources = await source_service.get_sources()
        existing_source_names = [source.name for source in existing_sources]

        for enum_source in SourceEnum:
            if enum_source not in existing_source_names:
                source = SourceCreate(name=enum_source)
                await source_service.add_source(source)

        await uow.commit()

    logger.info("Sources seeded")
