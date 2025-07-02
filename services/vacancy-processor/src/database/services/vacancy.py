from database.models import Vacancy
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["VacancyService"]


class VacancyService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_vacancy(self, vacancy: Vacancy) -> Vacancy:
        self.session.add(vacancy)
        await self.session.commit()
        await self.session.refresh(vacancy)

        return vacancy
