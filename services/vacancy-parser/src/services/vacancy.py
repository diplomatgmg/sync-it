from database.models.vacancy import BaseVacancy
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["find_duplicate_vacancy_by_fingerprint"]


SIMILARITY_THRESHOLD = 0.70


async def find_duplicate_vacancy_by_fingerprint(
    session: AsyncSession, model: type[BaseVacancy], fingerprint: str
) -> BaseVacancy | None:
    stmt = (
        select(model)
        .where(func.similarity(model.fingerprint, fingerprint) > SIMILARITY_THRESHOLD)
        .order_by(func.similarity(model.fingerprint, fingerprint).desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar()
