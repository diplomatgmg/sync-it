from clients import gpt_client, vacancy_client
from clients.schemas import VacancySchema
from common.logger import get_logger
from schemas.grade import GradeRead
from schemas.skill import SkillRead
from schemas.vacancy import VacancyCreate
from schemas.work_format import WorkFormatRead
from unitofwork import UnitOfWork
from utils.extractor import VacancyExtractor
from utils.prompter import make_prompt

from services import (
    GradeService,
    ProfessionService,
    SkillService,
    VacancyService,
    WorkFormatService,
)


__all__ = ["VacancyProcessor"]


logger = get_logger(__name__)


class VacancyProcessor:
    def __init__(
        self,
        uow: UnitOfWork,
        vacancy_extractor: VacancyExtractor,
        vacancy_service: VacancyService,
        grade_service: GradeService,
        profession_service: ProfessionService,
        work_format_service: WorkFormatService,
        skill_service: SkillService,
    ) -> None:
        self.uow = uow
        self.vacancy_extractor = vacancy_extractor
        self.vacancy_service = vacancy_service
        self.grade_service = grade_service
        self.profession_service = profession_service
        self.work_format_service = work_format_service
        self.skill_service = skill_service

    async def start(self) -> None:
        logger.debug("Start processing vacancies")
        vacancies = await vacancy_client.fetch()
        logger.info("Got %s new vacancies", len(vacancies))

        prompts = [make_prompt(vacancy.data) for vacancy in vacancies]

        for prompt, vacancy in zip(prompts, vacancies, strict=True):
            await self.process_prompt(prompt, vacancy)

    async def process_prompt(self, prompt: str, vacancy: VacancySchema) -> None:
        try:
            completion = await gpt_client.get_completion(prompt)

            bad_completions = (
                "Не вакансия",
                "It seems that this video doesn't have a transcript, please try another video",
            )
            if any(bad_completion in completion for bad_completion in bad_completions):
                logger.debug("Not a vacancy: %s", vacancy.link)
                await vacancy_client.delete(vacancy)
                return

            extracted_vacancy = self.vacancy_extractor.extract(completion)

            await self._save_vacancy_in_transaction(vacancy, extracted_vacancy)
            await self.uow.commit()
            await vacancy_client.delete(vacancy)
        except Exception as e:
            logger.exception("Failed to process vacancy %s", vacancy.link, exc_info=e)
            # Rollback произойдет автоматически при выходе из `get_async_session`
            return

    async def _save_vacancy_in_transaction(self, vacancy: VacancySchema, extracted_vacancy: VacancyExtractor) -> None:
        """Собирает и сохраняет модель вакансии в рамках переданной сессии."""
        logger.debug("Saving vacancy to session: %s", vacancy.link)

        profession_id = await self._resolve_profession_id(extracted_vacancy)
        grades = await self._resolve_grades(extracted_vacancy)
        work_formats = await self._resolve_work_formats(extracted_vacancy)
        skills = await self._resolve_skills(extracted_vacancy)

        vacancy_data = VacancyCreate(
            published_at=vacancy.published_at,
            hash=vacancy.hash,
            link=vacancy.link,
            company_name=extracted_vacancy.company_name,
            profession_id=profession_id,
            salary=extracted_vacancy.salary,
            workplace_description=extracted_vacancy.workplace_description,
            responsibilities=extracted_vacancy.responsibilities,
            requirements=extracted_vacancy.requirements,
            conditions=extracted_vacancy.conditions,
        )

        await self.vacancy_service.add_vacancy(vacancy_data, grades, work_formats, skills)

    async def _resolve_profession_id(self, extracted_vacancy: VacancyExtractor) -> int | None:
        profession_name = extracted_vacancy.profession
        if profession_name is None:
            return None

        profession = await self.profession_service.get_profession_by_name(profession_name)
        return profession.id if profession else None

    async def _resolve_grades(self, extracted_vacancy: VacancyExtractor) -> list[GradeRead]:
        grade_names = extracted_vacancy.grades
        grades: list[GradeRead] = []
        for name in grade_names:
            grade = await self.grade_service.get_grade_by_name(name)
            if grade:
                grades.append(grade)
        return grades

    async def _resolve_work_formats(self, extracted_vacancy: VacancyExtractor) -> list[WorkFormatRead]:
        work_format_names = extracted_vacancy.work_formats
        work_formats: list[WorkFormatRead] = []
        for name in work_format_names:
            work_format = await self.work_format_service.get_work_format_by_name(name)
            if work_format:
                work_formats.append(work_format)
        return work_formats

    async def _resolve_skills(self, extracted_vacancy: VacancyExtractor) -> list[SkillRead]:
        skill_names = [skill for _, skill in extracted_vacancy.skills]
        skills: list[SkillRead] = []
        for name in skill_names:
            skill = await self.skill_service.get_skill_by_name(name)
            if skill:
                skills.append(skill)
        return skills
