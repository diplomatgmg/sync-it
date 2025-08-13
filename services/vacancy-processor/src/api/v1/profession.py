from typing import Annotated

from api.depedencies import get_profession_service
from api.v1.schemas import ProfessionListResponse
from fastapi import APIRouter, Depends

from services import ProfessionService


__all__ = ["router"]


router = APIRouter()


@router.get("")
async def get_professions(
    service: Annotated[ProfessionService, Depends(get_profession_service)],
) -> ProfessionListResponse:
    """Возвращает актуальных профессий."""
    professions = await service.get_professions()

    return ProfessionListResponse(professions=professions)
