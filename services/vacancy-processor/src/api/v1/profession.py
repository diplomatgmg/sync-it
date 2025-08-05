from typing import Annotated

from common.database.engine import provide_async_session
from fastapi import APIRouter, Depends
from repositories import ProfessionRepository
from schemas import ProfessionModelResponse, ProfessionModelSchema
from sqlalchemy.ext.asyncio import AsyncSession

from services import ProfessionService


__all__ = ["router"]


router = APIRouter()


@router.get("/professions")
async def get_professions(session: Annotated[AsyncSession, Depends(provide_async_session)]) -> ProfessionModelResponse:
    """Возвращает актуальных профессий."""
    repo = ProfessionRepository(session)
    service = ProfessionService(repo)
    profession_models = await service.get_professions()

    return ProfessionModelResponse(professions=[ProfessionModelSchema.model_validate(p) for p in profession_models])
