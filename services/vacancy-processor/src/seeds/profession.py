from common.database.engine import get_async_session
from common.logger import get_logger
from database.enums import ProfessionEnum
from database.services import ProfessionService


__all__ = ["seed_professions"]


logger = get_logger(__name__)


async def seed_professions() -> None:
    logger.debug("Start seeding professions")

    async with get_async_session() as session:
        service = ProfessionService(session)
        existing_professions = await service.get_professions()
        existing_profession_names = [profession.name for profession in existing_professions]

        for enum_profession in ProfessionEnum:
            if enum_profession not in existing_profession_names:
                await service.add_profession(enum_profession)

    logger.info("Professions seeded")
