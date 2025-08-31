from collections.abc import Iterable, Sequence
from datetime import UTC, datetime, timedelta
import operator
from typing import Any, TypeVar

from common.logger import get_logger
from common.shared.repositories import BaseRepository
from database.models import Grade, Profession, Vacancy, WorkFormat
from database.models.enums import GradeEnum, ProfessionEnum, SkillEnum, WorkFormatEnum
from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload, selectinload


__all__ = ["VacancyRepository"]


logger = get_logger(__name__)

TSelect = TypeVar("TSelect", bound=Select[Any])


class VacancyRepository(BaseRepository):
    """Репозиторий для управления вакансиями."""

    MIN_SIMILARITY_PERCENT = 75  # Минимальное соотношение совпадающих навыков
    MIN_SKILLS_COUNT = 5
    BONUS_MIN_SKILL = 5  # Бонус за каждый навык сверх MIN_SKILLS_COUNT
    BEST_SKILLS_COUNT_BONUS = 10
    DAYS_INTERVAL = timedelta(days=30)

    async def add(self, vacancy: Vacancy) -> Vacancy:
        """Добавляет экземпляр вакансии в сессию."""
        self._session.add(vacancy)
        await self._session.flush()
        await self._session.refresh(vacancy, attribute_names=["profession", "skills", "grades", "work_formats"])

        return vacancy

    async def get_existing_hashes(self, hashes: Iterable[str]) -> set[str]:
        """Получить set уже существующих хешей в БД."""
        stmt = select(Vacancy.hash).where(Vacancy.hash.in_(hashes))
        result = await self._session.execute(stmt)

        return set(result.scalars().all())

    async def get_by_id(self, vacancy_id: int) -> Vacancy | None:
        """Получает вакансию по ее id."""
        stmt = select(Vacancy).where(Vacancy.id == vacancy_id)
        stmt = self._apply_vacancy_prefetch_details_to_stmt(stmt)
        result = await self._session.execute(stmt)

        return result.unique().scalar_one_or_none()

    async def get_all(self, limit: int) -> Sequence[Vacancy]:
        """Получает отфильтрованный список вакансий."""
        stmt = select(Vacancy)
        stmt = self._apply_vacancy_prefetch_details_to_stmt(stmt)
        stmt = stmt.order_by(Vacancy.published_at.desc()).limit(limit)

        result = await self._session.execute(stmt)

        return result.scalars().unique().all()

    async def get_relevant_with_neighbors(  # noqa: C901 PLR0912
        self,
        vacancy_id: int | None,
        professions: Sequence[ProfessionEnum],
        grades: Sequence[GradeEnum],
        work_formats: Sequence[WorkFormatEnum],
        skills: Sequence[SkillEnum],
    ) -> tuple[int | None, Vacancy | None, int | None]:
        """
        Находит вакансию по ID и ее соседей в списке, отсортированном по релевантности,
        выполняя все вычисления на стороне БД.
        """
        stmt = (
            select(Vacancy).where(Vacancy.published_at >= (datetime.now(UTC) - self.DAYS_INTERVAL)).order_by(Vacancy.id)
        )
        stmt = self._apply_vacancy_prefetch_details_to_stmt(stmt)

        if professions:
            stmt = stmt.join(Profession).filter(Profession.name.in_(professions))
        if grades:
            stmt = stmt.join(Vacancy.grades).filter(Grade.name.in_(grades))
        if work_formats:
            stmt = stmt.join(Vacancy.work_formats).filter(WorkFormat.name.in_(work_formats))

        result = await self._session.execute(stmt)
        vacancies = result.scalars().unique().all()

        scored_vacancies: list[tuple[float, Vacancy]] = []
        user_skills_set = set(skills)

        for vacancy in vacancies:
            vacancy_skills_set = {skill.name for skill in vacancy.skills}

            common_skills = user_skills_set & vacancy_skills_set
            if not common_skills:
                continue

            common_count = len(common_skills)

            similarity = (common_count / len(vacancy_skills_set)) * 100
            if similarity < self.MIN_SIMILARITY_PERCENT:
                continue

            # Бонус за превышение минимального количества навыков
            if common_count > self.MIN_SKILLS_COUNT:
                bonus = (common_count - self.MIN_SKILLS_COUNT) * self.BONUS_MIN_SKILL
                similarity += bonus

            # Бонус за идеальное совпадение (все навыки пользователя есть в вакансии)
            if user_skills_set.issubset(vacancy_skills_set):
                similarity += 10

            if similarity >= self.MIN_SIMILARITY_PERCENT:
                scored_vacancies.append((similarity, vacancy))

        if not scored_vacancies:
            return None, None, None

        scored_vacancies.sort(key=operator.itemgetter(0), reverse=True)
        sorted_vacancies = [v for _, v in scored_vacancies]

        if vacancy_id:
            try:
                index = next(i for i, v in enumerate(sorted_vacancies) if v.id == vacancy_id)
            except StopIteration:
                return None, None, None
        else:
            index = 0

        prev_id = sorted_vacancies[index - 1].id if index > 0 else None
        next_id = sorted_vacancies[index + 1].id if index < len(sorted_vacancies) - 1 else None

        return prev_id, sorted_vacancies[index], next_id

    @staticmethod
    def _apply_vacancy_prefetch_details_to_stmt(stmt: TSelect) -> TSelect:
        return stmt.options(
            joinedload(Vacancy.profession),
            selectinload(Vacancy.grades),
            selectinload(Vacancy.work_formats),
            selectinload(Vacancy.skills),
        )
