import asyncio

from common.logger import get_logger
from services.http import fetch_gpt_completion, fetch_new_vacancies
from services.prompter import make_prompt
from services.vacancy import VacancyExtractorService


__all__ = ["VacancyProcessorService"]


logger = get_logger(__name__)


class VacancyProcessorService:
    def __init__(self, extractor: VacancyExtractorService | None = None) -> None:
        self.extractor = extractor or VacancyExtractorService()

    async def start(self) -> None:
        logger.debug("Start processing vacancies")
        vacancies = await fetch_new_vacancies()
        logger.info("Got %s new vacancies", len(vacancies))

        prompts = [make_prompt(vacancy.data) for vacancy in vacancies]
        tasks = [self.process_prompt(prompt, vacancy.link) for prompt, vacancy in zip(prompts, vacancies, strict=True)]

        await asyncio.gather(*tasks)

    async def process_prompt(self, prompt: str, vacancy_link: str) -> None:
        try:
            completion = await fetch_gpt_completion(prompt)
            extracted_vacancy = self.extractor.extract(completion)
            logger.info("Extracted vacancy (%s): %s", vacancy_link, extracted_vacancy)
        except Exception as e:
            logger.exception("Failed to process vacancy %s", vacancy_link, exc_info=e)
            return
