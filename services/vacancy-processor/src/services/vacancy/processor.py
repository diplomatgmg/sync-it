import asyncio
from itertools import starmap

from common.logger import get_logger
from schemas import VacancySchema
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
        tasks = list(starmap(self.process_prompt, zip(prompts, vacancies, strict=True)))

        await asyncio.gather(*tasks)

    async def process_prompt(self, prompt: str, vacancy: VacancySchema) -> None:
        try:
            completion = await fetch_gpt_completion(prompt)
            if "Не вакансия" in completion:
                # TODO: реализовать модель parsed vacancy
                logger.debug("Not a vacancy: %s", vacancy.link)
                return

            extracted_vacancy = self.extractor.extract(completion)
            logger.debug("Extracted vacancy (%s):\n%s", vacancy.link, extracted_vacancy)
        except Exception as e:
            logger.exception("Failed to process vacancy %s", vacancy.link, exc_info=e)
            return

    async def save_vacancy(self, vacancy: VacancySchema) -> None:
        pass
