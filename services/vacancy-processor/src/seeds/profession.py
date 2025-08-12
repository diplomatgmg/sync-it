from common.logger import get_logger
from database.models.enums import ProfessionEnum
from schemas.profession import ProfessionCreate
from unitofwork import UnitOfWork

from services import ProfessionService


__all__ = ["seed_professions"]


logger = get_logger(__name__)


async def seed_professions() -> None:
    logger.debug("Start seeding professions")

    async with UnitOfWork() as uow:
        service = ProfessionService(uow)
        existing_professions = await service.get_professions()
        existing_profession_names = [profession.name for profession in existing_professions]

        for enum_profession in ProfessionEnum:
            if enum_profession not in existing_profession_names:
                profession = ProfessionCreate(name=enum_profession)
                await service.add_profession(profession)

        await uow.commit()

    logger.info("Professions seeded")
