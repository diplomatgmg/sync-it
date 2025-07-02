from celery_app import app, loop
from common.database.engine import get_async_session
from database.services import GradeService, ProfessionService, SkillService, WorkFormatService
from database.services.vacancy import VacancyService
from services.vacancy import VacancyExtractorService, VacancyProcessorService


__all__ = ["process_vacancies"]


@app.task(name="process_vacancies")  # type: ignore[misc]
def process_vacancies() -> None:
    loop.run_until_complete(async_process_vacancies())


async def async_process_vacancies() -> None:
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
