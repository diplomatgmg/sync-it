from typing import Annotated

from common.database.engine import provide_async_session
from fastapi import APIRouter, Depends
from repositories import SkillCategoryRepository, SkillRepository
from schemas import SkillCategoryModelSchema, SkillCategoryResponse, SkillModelSchema, SkillResponse
from sqlalchemy.ext.asyncio import AsyncSession

from services import SkillCategoryService, SkillService


__all__ = ["router"]


router = APIRouter()


@router.get("/skills")
async def get_skills(session: Annotated[AsyncSession, Depends(provide_async_session)]) -> SkillResponse:
    """Возвращает актуальные скиллы."""
    repo = SkillRepository(session)
    service = SkillService(repo)
    skill_models = await service.get_skills()

    return SkillResponse(skills=[SkillModelSchema.model_validate(s) for s in skill_models])


@router.post("/skills/categories")
async def get_skill_categories(
    session: Annotated[AsyncSession, Depends(provide_async_session)],
) -> SkillCategoryResponse:
    """Возвращает актуальные категории скиллов."""
    repo = SkillCategoryRepository(session)
    service = SkillCategoryService(repo)
    skill_category_models = await service.get_categories()

    return SkillCategoryResponse(categories=[SkillCategoryModelSchema.model_validate(c) for c in skill_category_models])
