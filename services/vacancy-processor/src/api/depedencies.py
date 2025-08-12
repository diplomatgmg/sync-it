from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from unitofwork import UnitOfWork

from services import GradeService, ProfessionService, WorkFormatService


__all__ = [
    "get_grade_service",
    "get_profession_service",
    "get_work_format_service",
]


async def _get_uow_session() -> AsyncGenerator[UnitOfWork]:
    """Зависимость для получения экземпляра Unit of Work."""
    uow = UnitOfWork()
    async with uow:
        yield uow


def get_profession_service(uow: Annotated[UnitOfWork, Depends(_get_uow_session)]) -> ProfessionService:
    """FastAPI зависимость для получения экземпляра сервиса BuildingService."""
    return ProfessionService(uow)


def get_grade_service(uow: Annotated[UnitOfWork, Depends(_get_uow_session)]) -> GradeService:
    """FastAPI зависимость для получения экземпляра сервиса GradeService."""
    return GradeService(uow)


def get_work_format_service(uow: Annotated[UnitOfWork, Depends(_get_uow_session)]) -> WorkFormatService:
    """FastAPI зависимость для получения экземпляра сервиса WorkFormatService."""
    return WorkFormatService(uow)
