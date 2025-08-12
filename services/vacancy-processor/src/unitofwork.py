from common.shared.unitofwork import BaseUnitOfWork
from repositories import ProfessionRepository


__all__ = ["UnitOfWork"]


class UnitOfWork(BaseUnitOfWork):
    """Конкретная реализация UoW для SQLAlchemy."""

    professions: ProfessionRepository

    def init_repositories(self) -> None:
        self.professions = ProfessionRepository(self._session)
