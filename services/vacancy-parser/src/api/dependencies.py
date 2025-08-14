from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from unitofwork import UnitOfWork

from services import VacancyService


__all__ = ["get_vacancy_service"]


async def _get_uow_session() -> AsyncGenerator[UnitOfWork]:
    """Зависимость для получения экземпляра Unit of Work."""
    uow = UnitOfWork()
    async with uow:
        yield uow


def get_vacancy_service(
    uow: Annotated[UnitOfWork, Depends(_get_uow_session)],
) -> VacancyService:
    """FastAPI зависимость для получения экземпляра сервиса VacancyService."""
    return VacancyService(uow)
