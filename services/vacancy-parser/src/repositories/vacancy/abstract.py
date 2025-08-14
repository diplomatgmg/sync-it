from collections.abc import Iterable, Sequence
from datetime import UTC, datetime

from common.shared.repositories import BaseRepository
from constants.fingerprint import FINGERPRINT_SIMILARITY_THRESHOLD
from database.models import Vacancy
from sqlalchemy import func, select, update


__all__ = ["AbstractVacancyRepository"]


class AbstractVacancyRepository[VacancyType: Vacancy = Vacancy](BaseRepository):
    """Абстрактный репозиторий для работы с моделями вакансий."""

    _model: type[VacancyType]

    async def get_recent_vacancies(self, limit: int = 100) -> Sequence[VacancyType]:
        """Получить последние актуальные вакансии."""
        stmt = (
            select(self._model)
            .where(self._model.deleted_at.is_(None))
            .order_by(self._model.published_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_existing_hashes(self, hashes: Iterable[str]) -> set[str]:
        """Получить set уже существующих хешей в БД."""
        stmt = select(self._model.hash).where(self._model.hash.in_(hashes))
        result = await self._session.execute(stmt)

        return set(result.scalars().all())

    async def find_duplicate_vacancy_by_fingerprint(self, fingerprint: str) -> VacancyType | None:
        """Найти дубликат вакансии по содержимому."""
        stmt = (
            select(self._model)
            .where(func.similarity(self._model.fingerprint, fingerprint) > FINGERPRINT_SIMILARITY_THRESHOLD)
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_similarity_score(self, fingerprint1: str, fingerprint2: str) -> float:
        """Получить % схожести между двумя fingerprint."""
        result = await self._session.execute(select(func.similarity(fingerprint1, fingerprint2)))
        similarity = result.scalar() or 0.0
        return round(similarity * 100, 2)

    async def add(self, vacancy: VacancyType) -> VacancyType:
        self._session.add(vacancy)
        await self._session.flush()
        await self._session.refresh(vacancy)

        return vacancy

    async def update_published_at(self, vacancy_hash: str, published_at: datetime) -> bool:
        """Обновляет дату публикации вакансии."""
        # Только для обновления. Используем Vacancy, а не self._model
        stmt = update(Vacancy).where(Vacancy.hash == vacancy_hash).values(published_at=published_at)
        result = await self._session.execute(stmt)
        return bool(result.rowcount)

    async def mark_as_deleted(self, vacancy_hash: str) -> bool:
        """
        Удаляет вакансию из первой подходящей таблицы по хешу.

        True - вакансия помечена как удаленная
        False - вакансия не найдена
        """
        # Только для удаления. Используем Vacancy, а не self._model
        stmt = (
            update(Vacancy)
            .where(Vacancy.hash == vacancy_hash)
            .where(Vacancy.deleted_at.is_(None))
            .values(deleted_at=datetime.now(tz=UTC))
        )
        result = await self._session.execute(stmt)
        return bool(result.rowcount)
