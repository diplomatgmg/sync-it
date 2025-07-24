from celery_app import app, loop

from services import VacancyExtractorService, VacancyProcessorService


__all__ = ["process_vacancies"]


@app.task(name="process_vacancies")  # type: ignore[misc]
def process_vacancies() -> None:
    loop.run_until_complete(async_process_vacancies())


async def async_process_vacancies() -> None:
    vacancy_extractor = VacancyExtractorService()
    processor_service = VacancyProcessorService(vacancy_extractor)
    await processor_service.start()
