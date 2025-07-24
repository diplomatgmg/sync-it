from typing import Annotated

from common.database.engine import provide_async_session
from common.logger import get_logger
from fastapi import APIRouter, Depends
from repositories.vacancy import VacancyRepository
from schemas import VacancyDeleteResponse, VacancyModelSchema, VacancyResponse
from services.vacancy import VacancyService
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["router"]


logger = get_logger(__name__)

router = APIRouter()


@router.get("/vacancies")
async def get_vacancies(session: Annotated[AsyncSession, Depends(provide_async_session)]) -> VacancyResponse:
    """Возвращает последние актуальные вакансии."""
    repo = VacancyRepository(session)
    service = VacancyService(repo)
    vacancy_models = await service.get_recent_vacancies()

    return VacancyResponse(vacancies=[VacancyModelSchema.model_validate(v) for v in vacancy_models])


@router.delete("/vacancies/{vacancy_hash}")
async def delete_vacancy(
    vacancy_hash: str,
    session: Annotated[AsyncSession, Depends(provide_async_session)],
) -> VacancyDeleteResponse:
    repo = VacancyRepository(session)
    service = VacancyService(repo)
    is_deleted = await service.mark_as_deleted(vacancy_hash)

    if is_deleted:
        await session.commit()

    return VacancyDeleteResponse(is_deleted=is_deleted)
