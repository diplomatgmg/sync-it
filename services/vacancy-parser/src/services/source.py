from common.shared.services.base import BaseUOWService
from database.models import Source
from schemas.source import SourceCreate, SourceRead
from unitofwork import UnitOfWork


__all__ = ["SourceService"]


class SourceService(BaseUOWService[UnitOfWork]):
    async def get_sources(self) -> list[SourceRead]:
        sources = await self._uow.sources.get_all()

        return [SourceRead.model_validate(s) for s in sources]

    async def add_source(self, source: SourceCreate) -> SourceRead:
        source_model = Source(name=source.name)
        created_source = await self._uow.sources.add(source_model)

        return SourceRead.model_validate(created_source)
