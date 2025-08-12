import asyncio
from itertools import starmap

from clients import gpt_client, vacancy_client
from common.database.engine import get_async_session
from common.logger import get_logger
from database.models import Grade, Skill, Vacancy, WorkFormat
from repositories import SkillRepository, VacancyRepository
from schemas.grade import GradeRead
from schemas.work_format import WorkFormatRead
from schemas_old import ParsedVacancySchema
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
    def __init__(self, vacancy_extractor: VacancyExtractor) -> None:
        self.vacancy_extractor = vacancy_extractor
        # lock для сохранения вакансий в БД
        self._db_lock = asyncio.Lock()

    async def start(self) -> None:
        logger.debug("Start processing vacancies")
        vacancies = await vacancy_client.fetch()
        logger.info("Got %s new vacancies", len(vacancies))

        prompts = [make_prompt(vacancy.data) for vacancy in vacancies]
        tasks = list(starmap(self.process_prompt, zip(prompts, vacancies, strict=True)))

        await asyncio.gather(*tasks)

    async def process_prompt(self, prompt: str, vacancy: ParsedVacancySchema) -> None:
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

            async with self._db_lock, get_async_session() as session, UnitOfWork() as uow:
                vacancy_repo = VacancyRepository(session)
                skill_repo = SkillRepository(session)

                vacancy_service = VacancyService(vacancy_repo)
                grade_service = GradeService(uow)
                profession_service = ProfessionService(uow)
                work_format_service = WorkFormatService(uow)
                skill_service = SkillService(skill_repo)

                # Выполняем всю логику сохранения в рамках одной транзакции
                await self._save_vacancy_in_transaction(
                    vacancy,
                    extracted_vacancy,
                    vacancy_service,
                    profession_service,
                    grade_service,
                    work_format_service,
                    skill_service,
                )
                # Коммитим изменения только после успешного выполнения
                await session.commit()

            # Удаляем вакансию из очереди только после успешного сохранения в БД
            await vacancy_client.delete(vacancy)
        except Exception as e:
            logger.exception("Failed to process vacancy %s", vacancy.link, exc_info=e)
            # Rollback произойдет автоматически при выходе из `get_async_session`
            return

    async def _save_vacancy_in_transaction(
        self,
        vacancy: ParsedVacancySchema,
        extracted_vacancy: VacancyExtractor,
        vacancy_service: VacancyService,
        profession_service: ProfessionService,
        grade_service: GradeService,
        work_format_service: WorkFormatService,
        skill_service: SkillService,
    ) -> None:
        """Собирает и сохраняет модель вакансии в рамках переданной сессии."""
        logger.debug("Saving vacancy to session: %s", vacancy.link)

        profession_id = await self._resolve_profession_id(extracted_vacancy, profession_service)
        grades = await self._resolve_grades(extracted_vacancy, grade_service)
        work_formats = await self._resolve_work_formats(extracted_vacancy, work_format_service)
        skills = await self._resolve_skills(extracted_vacancy, skill_service)

        # FIXME Use vacancy repo
        vacancy_model = Vacancy(
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

        # FIXME. Костыль пока все переписываю на UOW
        vacancy_model.grades = [Grade(id=grade.id, name=grade.name) for grade in grades]
        vacancy_model.work_formats = [WorkFormat(id=wf.id, name=wf.name) for wf in work_formats]
        vacancy_model.skills = skills

        # `add_vacancy` не должен содержать коммита
        await vacancy_service.add_vacancy(vacancy_model)

    @staticmethod
    async def _resolve_profession_id(
        extracted_vacancy: VacancyExtractor, profession_service: ProfessionService
    ) -> int | None:
        profession_name = extracted_vacancy.profession
        if profession_name is None:
            return None

        profession = await profession_service.get_profession_by_name(profession_name)
        return profession.id if profession else None

    @staticmethod
    async def _resolve_grades(extracted_vacancy: VacancyExtractor, grade_service: GradeService) -> list[GradeRead]:
        grade_names = extracted_vacancy.grades
        grades = []
        for name in grade_names:
            grade = await grade_service.get_grade_by_name(name)
            if grade:
                grades.append(grade)
        return grades

    @staticmethod
    async def _resolve_work_formats(
        extracted_vacancy: VacancyExtractor, work_format_service: WorkFormatService
    ) -> list[WorkFormatRead]:
        work_format_names = extracted_vacancy.work_formats
        work_formats = []
        for name in work_format_names:
            work_format = await work_format_service.get_work_format_by_name(name)
            if work_format:
                work_formats.append(work_format)
        return work_formats

    @staticmethod
    async def _resolve_skills(extracted_vacancy: VacancyExtractor, skill_service: SkillService) -> list[Skill]:
        skill_names = [skill for _, skill in extracted_vacancy.skills]
        skills = []
        for name in skill_names:
            skill = await skill_service.get_skill_by_name(name)
            if skill:
                skills.append(skill)
        return skills
