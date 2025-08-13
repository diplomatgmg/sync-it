from typing import Annotated

from api.depedencies import get_skill_category_service, get_skill_service
from api.v1.schemas import SkillCategoryListResponse, SkillListResponse
from fastapi import APIRouter, Depends, Query
from schemas.skill import SkillRead

from services import SkillCategoryService, SkillService


__all__ = ["router"]


router = APIRouter()


@router.get("")
async def get_skills(
    service: Annotated[SkillService, Depends(get_skill_service)],
    category_id: Annotated[int | None, Query()] = None,
) -> SkillListResponse:
    """Возвращает актуальные скиллы."""
    skills = await service.get_skills(category_id=category_id)

    return SkillListResponse(skills=[SkillRead.model_validate(s) for s in skills])


@router.get("/categories")
async def get_skill_categories(
    service: Annotated[SkillCategoryService, Depends(get_skill_category_service)],
) -> SkillCategoryListResponse:
    """Возвращает актуальные категории скиллов."""
    skill_categories = await service.get_categories()

    return SkillCategoryListResponse(skill_categories=skill_categories)
