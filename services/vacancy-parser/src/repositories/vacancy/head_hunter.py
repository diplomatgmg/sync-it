from database.models.enums import SourceEnum
from database.models.vacancy import HeadHunterVacancy
from repositories.vacancy.vacancy import VacancyRepository
from sqlalchemy import select


__all__ = ["HeadHunterVacancyRepository"]


class HeadHunterVacancyRepository(VacancyRepository):
    source = SourceEnum.HEAD_HUNTER
    model = HeadHunterVacancy

    async def get_vacancy_by_id(self, vacancy_id: int) -> HeadHunterVacancy | None:
        stmt = select(self.model).where(self.model.vacancy_id == vacancy_id)
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()
