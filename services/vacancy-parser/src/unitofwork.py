from common.shared.unitofwork import BaseUnitOfWork
from repositories import (
    SourceRepository,
)


__all__ = ["UnitOfWork"]


class UnitOfWork(BaseUnitOfWork):
    """Конкретная реализация UoW для SQLAlchemy."""

    sources: SourceRepository

    def init_repositories(self) -> None:
        self.sources = SourceRepository(self._session)
