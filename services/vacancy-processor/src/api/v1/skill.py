from typing import Annotated

from common.database.engine import provide_async_session
from database.services import SkillCategoryService, SkillService
from fastapi import APIRouter, Depends
from schemas import SkillCategoryModelSchema, SkillCategoryResponse, SkillModelSchema, SkillResponse
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["router"]


router = APIRouter()


@router.get("/skills")
async def get_skills(session: Annotated[AsyncSession, Depends(provide_async_session)]) -> SkillResponse:
    """Возвращает актуальные скиллы."""
    service = SkillService(session)
    skill_models = await service.get_skills()

    return SkillResponse(skills=[SkillModelSchema.model_validate(s) for s in skill_models])


@router.post("/skills/categories")
async def get_skill_categories(
    session: Annotated[AsyncSession, Depends(provide_async_session)],
) -> SkillCategoryResponse:
    """Возвращает актуальные категории скиллов."""
    service = SkillCategoryService(session)
    skill_category_models = await service.get_categories()

    return SkillCategoryResponse(categories=[SkillCategoryModelSchema.model_validate(c) for c in skill_category_models])
