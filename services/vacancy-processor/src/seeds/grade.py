from common.logger import get_logger
from database.models.enums import GradeEnum
from schemas.grade import GradeCreate
from services.grade import GradeService
from unitofwork import UnitOfWork


__all__ = ["seed_grades"]


logger = get_logger(__name__)


async def seed_grades() -> None:
    logger.debug("Start seeding grade")

    async with UnitOfWork() as uow:
        service = GradeService(uow)
        existing_grades = await service.get_grades()
        existing_grade_names = [grade.name for grade in existing_grades]

        for enum_grade in GradeEnum:
            if enum_grade not in existing_grade_names:
                grade = GradeCreate(name=enum_grade)
                await service.add_grade(grade)

        await uow.commit()

    logger.info("Grades seeded")
