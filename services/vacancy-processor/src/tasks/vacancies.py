from datetime import timedelta

from celery_app import app, loop
from common.shared.decorators.singleton import singleton
from unitofwork import UnitOfWork
from utils.extractor import VacancyExtractor
from utils.processor import VacancyProcessor

from services import GradeService, ProfessionService, SkillService, VacancyService, WorkFormatService


__all__ = ["process_vacancies"]


@app.task(name="process_vacancies")
@singleton(timedelta(minutes=30))
def process_vacancies() -> None:
    loop.run_until_complete(async_process_vacancies())


async def async_process_vacancies() -> None:
    extractor = VacancyExtractor()

    async with UnitOfWork() as uow:
        vacancy_service = VacancyService(uow)
        grade_service = GradeService(uow)
        profession_service = ProfessionService(uow)
        work_format_service = WorkFormatService(uow)
        skill_service = SkillService(uow)
        processor = VacancyProcessor(
            uow, extractor, vacancy_service, grade_service, profession_service, work_format_service, skill_service
        )
        await processor.start()
