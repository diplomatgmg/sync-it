from collections.abc import Sequence

from database.models import Profession
from database.models.enums import ProfessionEnum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["ProfessionService"]


class ProfessionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_profession_by_name(self, name: ProfessionEnum) -> Profession:
        stmt = select(Profession).where(Profession.name == name)
        result = await self.session.execute(stmt)

        return result.scalar_one()

    async def get_professions(self) -> Sequence[Profession]:
        stmt = select(Profession)
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def add_profession(self, profession: ProfessionEnum) -> Profession:
        profession_model = Profession(name=profession)

        self.session.add(profession_model)
        await self.session.commit()
        await self.session.refresh(profession_model)

        return profession_model
