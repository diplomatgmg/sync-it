from typing import Annotated

from common.database.engine import provide_async_session
from common.logger import get_logger
from database.services import SkillService
from fastapi import APIRouter, Depends
from schemas import SkillModelSchema, SkillResponse
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["router"]


logger = get_logger(__name__)

router = APIRouter()


@router.get("/skills")
async def get_skills(session: Annotated[AsyncSession, Depends(provide_async_session)]) -> SkillResponse:
    """Возвращает последние актуальные вакансии."""
    service = SkillService(session)
    skill_models = await service.get_skills()

    return SkillResponse(skills=[SkillModelSchema.model_validate(s) for s in skill_models])
