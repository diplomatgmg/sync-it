from collections.abc import Iterable, Sequence
from datetime import UTC, datetime

from common.logger import get_logger
from common.shared.repositories import BaseRepository
from constants.fingerprint import FINGERPRINT_SIMILARITY_THRESHOLD
from database.models import Vacancy
from sqlalchemy import func, select, update


__all__ = ["VacancyRepository"]


logger = get_logger(__name__)


class VacancyRepository(BaseRepository):
    """Репозиторий для работы с моделями вакансий."""

    async def get_recent_vacancies(self, limit: int = 100) -> Sequence[Vacancy]:
        """Получить последние актуальные вакансии."""
        stmt = select(Vacancy).where(Vacancy.deleted_at.is_(None)).order_by(Vacancy.published_at.desc()).limit(limit)
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def get_existing_hashes(self, hashes: Iterable[str]) -> set[str]:
        """Получить set уже существующих хешей в БД."""
        stmt = select(Vacancy.hash).where(Vacancy.hash.in_(hashes))
        result = await self._session.execute(stmt)

        return set(result.scalars().all())

    async def find_duplicate_vacancy_by_fingerprint(self, fingerprint: str) -> Vacancy | None:
        """Найти дубликат вакансии по содержимому."""
        stmt = (
            select(Vacancy)
            .where(func.similarity(Vacancy.fingerprint, fingerprint) > FINGERPRINT_SIMILARITY_THRESHOLD)
            .limit(1)
        )
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_similarity_score(self, fingerprint1: str, fingerprint2: str) -> float:
        """Получить % схожести между двумя fingerprint."""
        result = await self._session.execute(select(func.similarity(fingerprint1, fingerprint2)))
        similarity = result.scalar() or 0.0
        return round(similarity * 100, 2)

    async def update_published_at(self, vacancy_hash: str, published_at: datetime) -> bool:
        """Обновляет дату публикации вакансии."""
        stmt = update(Vacancy).where(Vacancy.hash == vacancy_hash).values(published_at=published_at)
        result = await self._session.execute(stmt)
        return bool(result.rowcount)

    async def mark_as_deleted(self, vacancy_hash: str) -> bool:
        """
        Удаляет вакансию из первой подходящей таблицы по хешу.

        True - вакансия помечена как удаленная
        False - вакансия не найдена
        """
        stmt = (
            update(Vacancy)
            .where(Vacancy.hash == vacancy_hash)
            .where(Vacancy.deleted_at.is_(None))
            .values(deleted_at=datetime.now(tz=UTC))
        )
        result = await self._session.execute(stmt)
        return bool(result.rowcount)
