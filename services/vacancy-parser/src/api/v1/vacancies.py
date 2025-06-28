from collections.abc import AsyncGenerator
from typing import Annotated

from common.database.engine import get_async_session
from common.logger import get_logger
from database.services.vacancy import VacancyService
from fastapi import APIRouter, Depends
from schemas import VacancyDeleteResponse, VacancyResponse
from serializers import VacancySerializer
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["router"]


logger = get_logger(__name__)

router = APIRouter()


async def _get_session() -> AsyncGenerator[AsyncSession]:
    async with get_async_session() as session:
        yield session


@router.get("/vacancies")
async def get_vacancies(session: Annotated[AsyncSession, Depends(_get_session)]) -> VacancyResponse:
    """Возвращает последние актуальные вакансии."""
    service = VacancyService(session)
    vacancy_models = await service.get_vacancies()

    return VacancyResponse(vacancies=[VacancySerializer.model_validate(v) for v in vacancy_models])


@router.delete("/vacancies/{vacancy_hash}")
async def delete_vacancy(
    vacancy_hash: str,
    session: Annotated[AsyncSession, Depends(_get_session)],
) -> VacancyDeleteResponse:
    service = VacancyService(session)
    is_deleted = await service.mark_as_deleted(vacancy_hash)

    return VacancyDeleteResponse(deleted=is_deleted)
