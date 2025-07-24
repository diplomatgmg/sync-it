from common.database.engine import get_async_session
from common.logger import get_logger
from database.models.enums import GradeEnum
from repositories import GradeRepository
from services.grade import GradeService


__all__ = ["seed_grades"]


logger = get_logger(__name__)


async def seed_grades() -> None:
    logger.debug("Start seeding grade")

    async with get_async_session() as session:
        repo = GradeRepository(session)
        service = GradeService(repo)
        existing_grades = await service.get_grades()
        existing_grade_names = [grade.name for grade in existing_grades]

        for enum_grade in GradeEnum:
            if enum_grade not in existing_grade_names:
                await service.add_grade(enum_grade)

        await session.commit()

    logger.info("Grades seeded")
