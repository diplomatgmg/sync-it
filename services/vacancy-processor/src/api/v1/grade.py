from typing import Annotated

from common.database.engine import provide_async_session
from fastapi import APIRouter, Depends
from repositories import GradeRepository
from schemas_old import GradeModelResponse, GradeModelSchema
from sqlalchemy.ext.asyncio import AsyncSession

from services import GradeService


__all__ = ["router"]


router = APIRouter()


@router.get("/grades")
async def get_grades(session: Annotated[AsyncSession, Depends(provide_async_session)]) -> GradeModelResponse:
    """Возвращает актуальных грейдов."""
    repo = GradeRepository(session)
    service = GradeService(repo)
    grade_models = await service.get_grades()

    return GradeModelResponse(grades=[GradeModelSchema.model_validate(g) for g in grade_models])
