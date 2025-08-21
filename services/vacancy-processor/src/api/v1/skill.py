from typing import Annotated

from api.depedencies import get_skill_service
from api.v1.schemas import SkillListResponse
from fastapi import APIRouter, Depends
from schemas.skill import SkillRead

from services import SkillService


__all__ = ["router"]


router = APIRouter()


@router.get("")
async def get_skills(service: Annotated[SkillService, Depends(get_skill_service)]) -> SkillListResponse:
    """Возвращает актуальные скиллы."""
    skills = await service.get_skills()

    return SkillListResponse(skills=[SkillRead.model_validate(s) for s in skills])
