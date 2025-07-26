from celery_app import app, loop
from utils.extractor import VacancyExtractor
from utils.processor import VacancyProcessor


__all__ = ["process_vacancies"]


@app.task(name="process_vacancies")  # type: ignore[misc]
def process_vacancies() -> None:
    loop.run_until_complete(async_process_vacancies())


async def async_process_vacancies() -> None:
    extractor = VacancyExtractor()
    processor = VacancyProcessor(extractor)
    await processor.start()
