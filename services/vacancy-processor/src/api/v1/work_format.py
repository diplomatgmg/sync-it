from typing import Annotated

from api.depedencies import get_work_format_service
from api.v1.schemas import WorkFormatListResponse
from fastapi import APIRouter, Depends

from services import WorkFormatService


__all__ = ["router"]


router = APIRouter()


@router.get("")
async def get_work_formats(
    service: Annotated[WorkFormatService, Depends(get_work_format_service)],
) -> WorkFormatListResponse:
    """Возвращает актуальных форматов работы."""
    work_formats = await service.get_work_formats()

    return WorkFormatListResponse(work_formats=work_formats)
