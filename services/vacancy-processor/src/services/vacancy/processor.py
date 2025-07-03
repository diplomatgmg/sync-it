import asyncio
from itertools import starmap

from common.logger import get_logger
from database.models import Grade, Skill, Vacancy, WorkFormat
from database.services import GradeService, ProfessionService, SkillService, WorkFormatService
from database.services.vacancy import VacancyService
from schemas import VacancySchema
from services.http import fetch_gpt_completion, fetch_new_vacancies, send_delete_request_vacancy
from services.prompter import make_prompt
from services.vacancy import VacancyExtractorService


__all__ = ["VacancyProcessorService"]


logger = get_logger(__name__)


class VacancyProcessorService:
    def __init__(
        self,
        vacancy_extractor: VacancyExtractorService,
        vacancy_service: VacancyService,
        profession_service: ProfessionService,
        grade_service: GradeService,
        work_format_service: WorkFormatService,
        skill_service: SkillService,
    ) -> None:
        self.vacancy_extractor = vacancy_extractor
        # DB depends services
        self.vacancy_service = vacancy_service
        self.profession_service = profession_service
        self.grade_service = grade_service
        self.work_format_service = work_format_service
        self.skill_service = skill_service

        # lock для сохранения вакансий в БД
        self._db_lock = asyncio.Lock()

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

            bad_completions = (
                "Не вакансия",
                "It seems that this video doesn't have a transcript, please try another video",
            )
            if any(bad_completion in completion for bad_completion in bad_completions):
                logger.debug("Not a vacancy: %s", vacancy.link)
                await send_delete_request_vacancy(vacancy)
                return

            extracted_vacancy = self.vacancy_extractor.extract(completion)

            async with self._db_lock:
                await self.save_vacancy(vacancy, extracted_vacancy)

            # В случае ошибка вакансия сохраняется в БД, но не пометится как удаленная и появится дубль
            await send_delete_request_vacancy(vacancy)
        except Exception as e:
            logger.exception("Failed to process vacancy %s", vacancy.link, exc_info=e)
            return

    async def save_vacancy(self, vacancy: VacancySchema, extracted_vacancy: VacancyExtractorService) -> None:
        logger.debug("Saving vacancy: %s", vacancy.link)

        profession_id = await self._resolve_profession_id(extracted_vacancy)

        vacancy_model = Vacancy(
            hash=vacancy.hash,
            link=vacancy.link,
            profession_id=profession_id,
            workplace_description=extracted_vacancy.workplace_description,
            responsibilities=extracted_vacancy.responsibilities,
            requirements=extracted_vacancy.requirements,
            conditions=extracted_vacancy.conditions,
        )

        vacancy_model.grades = await self._resolve_grades(extracted_vacancy)
        vacancy_model.work_formats = await self._resolve_work_formats(extracted_vacancy)
        vacancy_model.skills = await self._resolve_skills(extracted_vacancy)

        await self.vacancy_service.add_vacancy(vacancy_model)

    async def _resolve_profession_id(self, extracted_vacancy: VacancyExtractorService) -> int | None:
        profession_name = extracted_vacancy.profession
        if profession_name is None:
            return None

        profession = await self.profession_service.get_profession_by_name(profession_name)
        return profession.id

    async def _resolve_grades(self, extracted_vacancy: VacancyExtractorService) -> list[Grade]:
        grade_names = extracted_vacancy.grades
        grades = []

        for name in grade_names:
            grade = await self.grade_service.get_grade_by_name(name)
            grades.append(grade)

        return grades

    async def _resolve_work_formats(self, extracted_vacancy: VacancyExtractorService) -> list[WorkFormat]:
        work_format_names = extracted_vacancy.work_formats
        work_formats = []

        for name in work_format_names:
            work_format = await self.work_format_service.get_work_format_by_name(name)
            work_formats.append(work_format)

        return work_formats

    async def _resolve_skills(self, extracted_vacancy: VacancyExtractorService) -> list[Skill]:
        skill_names = [skill for _, skill in extracted_vacancy.skills]
        skills = []

        for name in skill_names:
            skill = await self.skill_service.get_skill_by_name(name)
            skills.append(skill)

        return skills
