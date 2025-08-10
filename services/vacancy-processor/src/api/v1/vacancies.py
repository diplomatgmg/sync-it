from typing import Annotated

from common.database.engine import provide_async_session
from common.logger import get_logger
from database.models.enums import GradeEnum, ProfessionEnum, SkillEnum, WorkFormatEnum
from fastapi import APIRouter, Depends, Path, Query
from repositories import VacancyRepository
from schemas import (
    ProcessedVacancyModelSchema,
    VacancyModelResponse,
    VacancyWithNeighborsResponse,
    VacancyWithNeighborsSchema,
)
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
    skills: Annotated[list[SkillEnum] | None, Query()] = None,
    limit: int | None = None,
) -> VacancyModelResponse:
    """Получить список актуальных вакансий, подходящих под заданные фильтры."""
    repo = VacancyRepository(session)
    service = VacancyService(repo)
    vacancy_models = await service.get_vacancies(
        professions,
        grades,
        work_formats,
        skills=skills,
        limit=limit,
    )

    return VacancyModelResponse(vacancies=[ProcessedVacancyModelSchema.model_validate(v) for v in vacancy_models])


@router.get("/vacancies/{vacancy_id}")
async def get_vacancy_with_neighbors(
    vacancy_id: Annotated[
        int,
        Path(
            description="ID вакансии. Укажите -1, чтобы получить самую последнюю вакансию включая фильтрацию.",
        ),
    ],
    session: Annotated[AsyncSession, Depends(provide_async_session)],
    professions: Annotated[list[ProfessionEnum] | None, Query()] = None,
    grades: Annotated[list[GradeEnum] | None, Query()] = None,
    work_formats: Annotated[list[WorkFormatEnum] | None, Query()] = None,
    skills: Annotated[list[SkillEnum] | None, Query()] = None,
) -> VacancyWithNeighborsResponse:
    repo = VacancyRepository(session)
    service = VacancyService(repo)

    prev_id, vacancy, next_id = await service.get_vacancy_with_neighbors(
        vacancy_id, professions, grades, work_formats, skills
    )

    result = VacancyWithNeighborsSchema(
        prev_id=prev_id,
        next_id=next_id,
        vacancy=ProcessedVacancyModelSchema.model_validate(vacancy) if vacancy else None,
    )
    return VacancyWithNeighborsResponse(result=result)
