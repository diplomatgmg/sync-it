from typing import Annotated

from api.depedencies import get_vacancy_service
from api.v1.schemas import VacancyListResponse, VacancyWithNeighborsResponse, VacancyWithNeighborsSchema
from common.logger import get_logger
from database.models.enums import GradeEnum, ProfessionEnum, SkillEnum, WorkFormatEnum
from fastapi import APIRouter, Depends, Path, Query

from services import VacancyService


__all__ = ["router"]


logger = get_logger(__name__)
router = APIRouter()


@router.get("")
async def get_vacancies(
    service: Annotated[VacancyService, Depends(get_vacancy_service)],
    professions: Annotated[list[ProfessionEnum] | None, Query()] = None,
    grades: Annotated[list[GradeEnum] | None, Query()] = None,
    work_formats: Annotated[list[WorkFormatEnum] | None, Query()] = None,
    skills: Annotated[list[SkillEnum] | None, Query()] = None,
    limit: int | None = None,
) -> VacancyListResponse:
    """Получить список актуальных вакансий, подходящих под заданные фильтры."""
    vacancies = await service.get_vacancies(
        professions,
        grades,
        work_formats,
        skills=skills,
        limit=limit,
    )

    return VacancyListResponse(vacancies=vacancies)


@router.get("/{vacancy_id}")
async def get_vacancy_with_neighbors(
    service: Annotated[VacancyService, Depends(get_vacancy_service)],
    vacancy_id: Annotated[
        int,
        Path(
            description="ID вакансии. Укажите -1, чтобы получить самую последнюю вакансию с заданными фильтрами.",
        ),
    ],
    professions: Annotated[list[ProfessionEnum] | None, Query()] = None,
    grades: Annotated[list[GradeEnum] | None, Query()] = None,
    work_formats: Annotated[list[WorkFormatEnum] | None, Query()] = None,
    skills: Annotated[list[SkillEnum] | None, Query()] = None,
) -> VacancyWithNeighborsResponse:
    prev_id, vacancy, next_id = await service.get_vacancy_with_neighbors(
        vacancy_id, professions, grades, work_formats, skills
    )

    result = VacancyWithNeighborsSchema(
        prev_id=prev_id,
        next_id=next_id,
        vacancy=vacancy,
    )

    return VacancyWithNeighborsResponse(result=result)
