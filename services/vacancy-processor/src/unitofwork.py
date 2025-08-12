from common.shared.unitofwork import BaseUnitOfWork
from repositories import GradeRepository, ProfessionRepository


__all__ = ["UnitOfWork"]


class UnitOfWork(BaseUnitOfWork):
    """Конкретная реализация UoW для SQLAlchemy."""

    professions: ProfessionRepository
    grades: GradeRepository

    def init_repositories(self) -> None:
        self.professions = ProfessionRepository(self._session)
        self.grades = GradeRepository(self._session)
