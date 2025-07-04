from common.database.engine import get_async_session
from common.logger import get_logger
from database.models.enums import SourceEnum
from database.services import SourceService


__all__ = ["seed_sources"]


logger = get_logger(__name__)


async def seed_sources() -> None:
    logger.debug("Start seeding sources")

    async with get_async_session() as session:
        service = SourceService(session)
        existing_sources = await service.get_sources()
        existing_source_names = [source.name for source in existing_sources]

        for enum_source in SourceEnum:
            if enum_source not in existing_source_names:
                await service.add_source(enum_source)

    logger.info("Sources seeded")
