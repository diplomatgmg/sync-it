from collections.abc import AsyncGenerator
from typing import Annotated

from common.database.engine import get_async_session
from common.logger import get_logger
from database.services.vacancy import VacancyService
from fastapi import APIRouter, Depends
from serializers import VacancySerializer
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["router"]


logger = get_logger(__name__)

router = APIRouter()


async def _get_session() -> AsyncGenerator[AsyncSession]:
    async with get_async_session() as session:
        yield session


@router.get("/vacancies")
async def get_newest_vacancies(db: Annotated[AsyncSession, Depends(_get_session)]) -> list[VacancySerializer]:
    """Возвращает последние актуальные вакансии."""
    service = VacancyService(db)
    vacancies = await service.get_vacancies()

    return [VacancySerializer.model_validate(v) for v in vacancies]
