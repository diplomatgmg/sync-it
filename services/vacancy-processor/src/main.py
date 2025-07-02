from common.database.engine import get_async_session
from common.logger import get_logger
from database.services import GradeService, ProfessionService, SkillService, WorkFormatService
from database.services.vacancy import VacancyService
from seeds import seed_models
from services.vacancy import VacancyExtractorService, VacancyProcessorService
import uvloop


logger = get_logger(__name__)


async def main() -> None:
    await seed_models()

    async with get_async_session() as session:
        vacancy_extractor = VacancyExtractorService()

        vacancy_service = VacancyService(session)
        profession_service = ProfessionService(session)
        grade_service = GradeService(session)
        work_format_service = WorkFormatService(session)
        skill_service = SkillService(session)

        processor_service = VacancyProcessorService(
            vacancy_extractor,
            vacancy_service,
            profession_service,
            grade_service,
            work_format_service,
            skill_service,
        )
        await processor_service.start()


if __name__ == "__main__":
    uvloop.run(main())
