from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from unitofwork import UnitOfWork

from services import ProfessionService


__all__ = [
    "get_profession_service",
]


async def _get_uow_session() -> AsyncGenerator[UnitOfWork]:
    """Зависимость для получения экземпляра Unit of Work."""
    uow = UnitOfWork()
    async with uow:
        yield uow


def get_profession_service(uow: Annotated[UnitOfWork, Depends(_get_uow_session)]) -> ProfessionService:
    """FastAPI зависимость для получения экземпляра сервиса BuildingService."""
    return ProfessionService(uow)
