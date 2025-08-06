from collections.abc import Iterable, Sequence
from datetime import UTC, datetime

from common.logger import get_logger
from common.shared.repositories import BaseRepository
from database.models import Source
from database.models.enums import SourceEnum
from database.models.vacancy import BaseVacancy
from sqlalchemy import func, select, update


__all__ = ["VacancyRepository"]


logger = get_logger(__name__)


# TODO: вынести в конфиг?
SIMILARITY_THRESHOLD = 0.70


class VacancyRepository(BaseRepository):
    """Репозиторий для работы с моделями вакансий."""

    source: SourceEnum
    model: type[BaseVacancy]

    __source_id: int | None = None

    async def get_source_id(self) -> int:
        if self.__source_id is not None:
            return self.__source_id

        stmt = select(Source.id).where(Source.name == self.source)
        result = await self._session.execute(stmt)
        source_id = result.scalar_one()

        self.__source_id = source_id

        return source_id

    async def get_recent_vacancies(self, limit: int = 100) -> Sequence[BaseVacancy]:
        """Получить последние актуальные вакансии по всем сервисам."""
        vacancies: list[BaseVacancy] = []

        subclasses = BaseVacancy.__subclasses__()

        for subclass in subclasses:
            stmt = (
                select(subclass)
                .where(subclass.deleted_at.is_(None))
                .order_by(subclass.published_at.desc())
                .limit(limit)
            )
            result = await self._session.execute(stmt)
            vacancies.extend(result.scalars().all())

        vacancies.sort(key=lambda x: x.published_at, reverse=True)
        return vacancies[:limit]

    async def bulk_create(self, vacancies: Sequence[BaseVacancy]) -> int:
        """Массовое добавление вакансий."""
        self._session.add_all(vacancies)
        return len(vacancies)

    async def mark_as_deleted(self, vacancy_hash: str) -> bool:
        """
        Удаляет вакансию из первой подходящей таблицы по хешу.

        True - вакансия помечена как удаленная
        False - вакансия не найдена
        """
        for subclass in BaseVacancy.__subclasses__():
            stmt = (
                update(subclass)
                .where(subclass.hash == vacancy_hash)
                .where(subclass.deleted_at.is_(None))
                .values(deleted_at=datetime.now(tz=UTC))
            )
            result = await self._session.execute(stmt)
            if bool(result.rowcount):
                logger.debug("Marked as deleted vacancy with hash %s", vacancy_hash)
                return True

        logger.debug("Not found vacancy with hash %s", vacancy_hash)
        return False

    async def get_existing_hashes(self, hashes: Iterable[str]) -> set[str]:
        """Получить set уже существующих хешей в БД."""
        stmt = select(self.model.hash).where(self.model.hash.in_(hashes))
        result = await self._session.execute(stmt)
        return {row[0] for row in result.fetchall()}

    async def find_duplicate_vacancy_by_fingerprint(self, fingerprint: str) -> BaseVacancy | None:
        """Найти дубликат вакансии по содержимому."""

        stmt = (
            select(self.model)
            .where(func.similarity(self.model.fingerprint, fingerprint) > SIMILARITY_THRESHOLD)
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_similarity_score(self, fingerprint1: str, fingerprint2: str) -> float:
        """Получить % схожести между двумя fingerprint."""
        result = await self._session.execute(select(func.similarity(fingerprint1, fingerprint2)))
        score = result.scalar() or 0.0
        return round(score * 100, 2)
