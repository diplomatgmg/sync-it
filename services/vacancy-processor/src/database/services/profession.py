from collections.abc import Sequence

from database.enums import ProfessionEnum
from database.models import Profession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ProfessionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

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
