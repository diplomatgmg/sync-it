from typing import Annotated

from common.database.engine import provide_async_session
from fastapi import APIRouter, Depends, Query
from repositories import SkillCategoryRepository, SkillRepository
from schemas_old import SkillCategoryModelResponse, SkillCategoryModelSchema, SkillModelResponse, SkillModelSchema
from sqlalchemy.ext.asyncio import AsyncSession

from services import SkillCategoryService, SkillService


__all__ = ["router"]


router = APIRouter()


@router.get("/skills")
async def get_skills(
    session: Annotated[AsyncSession, Depends(provide_async_session)],
    category_id: Annotated[int | None, Query()] = None,
) -> SkillModelResponse:
    """Возвращает актуальные скиллы."""
    repo = SkillRepository(session)
    service = SkillService(repo)
    skill_models = await service.get_skills(category_id=category_id)

    return SkillModelResponse(skills=[SkillModelSchema.model_validate(s) for s in skill_models])


@router.get("/skills/categories")
async def get_skill_categories(
    session: Annotated[AsyncSession, Depends(provide_async_session)],
) -> SkillCategoryModelResponse:
    """Возвращает актуальные категории скиллов."""
    repo = SkillCategoryRepository(session)
    service = SkillCategoryService(repo)
    skill_category_models = await service.get_categories()
    skill_category_schemas = [SkillCategoryModelSchema.model_validate(c) for c in skill_category_models]

    return SkillCategoryModelResponse(categories=skill_category_schemas)
