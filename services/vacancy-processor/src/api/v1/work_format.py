from typing import Annotated

from common.database.engine import provide_async_session
from database.services import WorkFormatService
from fastapi import APIRouter, Depends
from schemas import WorkFormatModelSchema, WorkFormatResponse
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["router"]


router = APIRouter()


@router.get("/work_formats")
async def get_work_formats(session: Annotated[AsyncSession, Depends(provide_async_session)]) -> WorkFormatResponse:
    """Возвращает актуальных форматов работы."""
    service = WorkFormatService(session)
    work_format_models = await service.get_work_formats()

    return WorkFormatResponse(work_formats=[WorkFormatModelSchema.model_validate(w) for w in work_format_models])
