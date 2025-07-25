from collections.abc import Sequence

from common.shared.services import BaseService
from database.models import Source
from database.models.enums import SourceEnum
from repositories import SourceRepository


__all__ = ["SourceService"]


class SourceService(BaseService[SourceRepository]):
    async def get_sources(self) -> Sequence[Source]:
        return await self._repo.get_all()

    async def add_source(self, source_enum: SourceEnum) -> Source:
        source_model = Source(name=source_enum)

        return await self._repo.create(source_model)
