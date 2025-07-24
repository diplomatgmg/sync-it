from typing import Annotated

from common.database.engine import provide_async_session
from fastapi import APIRouter, Depends
from repositories import WorkFormatRepository
from schemas import WorkFormatModelSchema, WorkFormatResponse
from sqlalchemy.ext.asyncio import AsyncSession

from services import WorkFormatService


__all__ = ["router"]


router = APIRouter()


@router.get("/work_formats")
async def get_work_formats(session: Annotated[AsyncSession, Depends(provide_async_session)]) -> WorkFormatResponse:
    """Возвращает актуальных форматов работы."""
    repo = WorkFormatRepository(session)
    service = WorkFormatService(repo)
    work_format_models = await service.get_work_formats()

    return WorkFormatResponse(work_formats=[WorkFormatModelSchema.model_validate(w) for w in work_format_models])
