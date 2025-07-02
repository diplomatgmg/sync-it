from typing import Annotated

from common.database.engine import provide_async_session
from database.services import ProfessionService
from fastapi import APIRouter, Depends
from schemas import ProfessionModelSchema, ProfessionResponse
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["router"]


router = APIRouter()


@router.get("/professions")
async def get_grades(session: Annotated[AsyncSession, Depends(provide_async_session)]) -> ProfessionResponse:
    """Возвращает актуальных профессий."""
    service = ProfessionService(session)
    profession_models = await service.get_professions()

    return ProfessionResponse(professions=[ProfessionModelSchema.model_validate(p) for p in profession_models])
