from collections.abc import Sequence

from database.models import Source
from database.models.enums import SourceEnum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["SourceService"]


class SourceService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_sources(self) -> Sequence[Source]:
        stmt = select(Source)
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def add_source(self, source: SourceEnum) -> Source:
        source_model = Source(name=source)

        self.session.add(source_model)
        await self.session.commit()
        await self.session.refresh(source_model)

        return source_model
