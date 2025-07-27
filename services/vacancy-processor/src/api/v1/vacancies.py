from typing import Annotated

from common.database.engine import provide_async_session
from common.logger import get_logger
from database.models.enums import GradeEnum, ProfessionEnum, WorkFormatEnum
from fastapi import APIRouter, Depends, Query
from repositories import VacancyRepository
from schemas import ProcessedVacancyModelSchema, VacancyModelResponse
from sqlalchemy.ext.asyncio import AsyncSession

from services import VacancyService


__all__ = ["router"]


logger = get_logger(__name__)
router = APIRouter()


@router.get("/vacancies")
async def get_vacancies(
    session: Annotated[AsyncSession, Depends(provide_async_session)],
    professions: Annotated[list[ProfessionEnum] | None, Query()] = None,
    grades: Annotated[list[GradeEnum] | None, Query()] = None,
    work_formats: Annotated[list[WorkFormatEnum] | None, Query()] = None,
) -> VacancyModelResponse:
    """Получить список актуальных вакансий, подходящих под заданные фильтры."""
    repo = VacancyRepository(session)
    service = VacancyService(repo)
    vacancy_models = await service.get_vacancies(
        professions,
        grades,
        work_formats,
    )

    return VacancyModelResponse(vacancies=[ProcessedVacancyModelSchema.model_validate(v) for v in vacancy_models])
