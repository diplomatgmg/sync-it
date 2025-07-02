from typing import Annotated

from common.database.engine import provide_async_session
from database.services import GradeService
from fastapi import APIRouter, Depends
from schemas import GradeModelSchema, GradeResponse
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["router"]


router = APIRouter()


@router.get("/grades")
async def get_grades(session: Annotated[AsyncSession, Depends(provide_async_session)]) -> GradeResponse:
    """Возвращает актуальных грейдов."""
    service = GradeService(session)
    grade_models = await service.get_grades()

    return GradeResponse(grades=[GradeModelSchema.model_validate(g) for g in grade_models])
