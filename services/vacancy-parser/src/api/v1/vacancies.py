from typing import Annotated

from api.dependencies import get_vacancy_service
from api.v1.schemas import VacancyDeleteResponse, VacancyListResponse
from fastapi import APIRouter, Depends
from schemas.vacancy import VacancyCreate, VacancyRead

from services import VacancyService


__all__ = ["router"]


router = APIRouter()


@router.get("/vacancies")
async def get_vacancies(
    service: Annotated[VacancyService[VacancyRead, VacancyCreate], Depends(get_vacancy_service)],
) -> VacancyListResponse:
    """Возвращает последние актуальные вакансии."""
    vacancies = await service.get_recent_vacancies()

    return VacancyListResponse(vacancies=vacancies)


@router.delete("/vacancies/{vacancy_hash}")
async def delete_vacancy(
    vacancy_hash: str,
    service: Annotated[VacancyService[VacancyRead, VacancyCreate], Depends(get_vacancy_service)],
) -> VacancyDeleteResponse:
    is_deleted = await service.mark_as_deleted(vacancy_hash)

    await service.commit()

    return VacancyDeleteResponse(is_deleted=is_deleted)
