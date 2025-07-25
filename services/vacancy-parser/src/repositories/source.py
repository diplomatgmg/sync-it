from collections.abc import Sequence

from common.shared.repositories import BaseRepository
from database.models import Source
from sqlalchemy import select


__all__ = ["SourceRepository"]


class SourceRepository(BaseRepository):
    async def get_all(self) -> Sequence[Source]:
        stmt = select(Source)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def create(self, source: Source) -> Source:
        self._session.add(source)
        await self._session.commit()
        await self._session.refresh(source)
        return source
