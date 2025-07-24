from collections.abc import Sequence

from database.models import Source
from database.models.enums import SourceEnum
from repositories import SourceRepository


__all__ = ["SourceService"]


class SourceService:
    def __init__(self, source_repository: SourceRepository) -> None:
        self.repo = source_repository

    async def get_sources(self) -> Sequence[Source]:
        return await self.repo.get_all()

    async def add_source(self, source_enum: SourceEnum) -> Source:
        source_model = Source(name=source_enum)

        return await self.repo.create(source_model)
