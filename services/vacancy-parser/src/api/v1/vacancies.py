from typing import Annotated

from api.dependencies import get_vacancy_service
from api.v1.schemas import VacancyDeleteResponse, VacancyListResponse
from common.logger import get_logger
from fastapi import APIRouter, Depends

from services import VacancyService


__all__ = ["router"]


logger = get_logger(__name__)

router = APIRouter()


@router.get("/vacancies")
async def get_vacancies(service: Annotated[VacancyService, Depends(get_vacancy_service)]) -> VacancyListResponse:
    """Возвращает последние актуальные вакансии."""
    vacancies = await service.get_recent_vacancies()

    return VacancyListResponse(vacancies=vacancies)


@router.delete("/vacancies/{vacancy_hash}")
async def delete_vacancy(
    vacancy_hash: str,
    service: Annotated[VacancyService, Depends(get_vacancy_service)],
) -> VacancyDeleteResponse:
    is_deleted = await service.mark_as_deleted(vacancy_hash)

    return VacancyDeleteResponse(is_deleted=is_deleted)
