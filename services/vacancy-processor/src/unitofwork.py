from common.shared.unitofwork import BaseUnitOfWork
from repositories import (
    GradeRepository,
    ProfessionRepository,
    SkillRepository,
    VacancyRepository,
    WorkFormatRepository,
)


__all__ = ["UnitOfWork"]


class UnitOfWork(BaseUnitOfWork):
    """Конкретная реализация UoW для SQLAlchemy."""

    professions: ProfessionRepository
    grades: GradeRepository
    work_formats: WorkFormatRepository
    skills: SkillRepository
    vacancies: VacancyRepository

    def init_repositories(self) -> None:
        self.professions = ProfessionRepository(self._session)
        self.grades = GradeRepository(self._session)
        self.work_formats = WorkFormatRepository(self._session)
        self.skills = SkillRepository(self._session)
        self.vacancies = VacancyRepository(self._session)
