from typing import Annotated

from api.depedencies import get_grade_service
from api.v1.schemas import GradeListResponse
from fastapi import APIRouter, Depends

from services import GradeService


__all__ = ["router"]


router = APIRouter()


@router.get("")
async def get_grades(service: Annotated[GradeService, Depends(get_grade_service)]) -> GradeListResponse:
    """Возвращает актуальных грейдов."""
    grades = await service.get_grades()

    return GradeListResponse(grades=grades)
