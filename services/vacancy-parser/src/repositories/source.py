from collections.abc import Sequence

from database.models import Source
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["SourceRepository"]


class SourceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> Sequence[Source]:
        stmt = select(Source)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, source: Source) -> Source:
        self.session.add(source)
        await self.session.commit()
        await self.session.refresh(source)
        return source
