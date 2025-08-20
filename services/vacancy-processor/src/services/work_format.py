from async_lru import alru_cache
from common.shared.services import BaseUOWService
from database.models import WorkFormat
from database.models.enums import WorkFormatEnum
from schemas.work_format import WorkFormatCreate, WorkFormatRead
from unitofwork import UnitOfWork


__all__ = ["WorkFormatService"]


class WorkFormatService(BaseUOWService[UnitOfWork]):
    """Сервис для бизнес-операций, связанных с форматами работы."""

    @alru_cache
    async def get_work_format_by_name(self, name: WorkFormatEnum) -> WorkFormatRead:
        work_format = await self._uow.work_formats.get_by_name(name)

        return WorkFormatRead.model_validate(work_format)

    async def get_work_formats(self) -> list[WorkFormatRead]:
        work_formats = await self._uow.work_formats.get_all()

        return [WorkFormatRead.model_validate(wf) for wf in work_formats]

    async def add_work_format(self, work_format: WorkFormatCreate) -> WorkFormatRead:
        work_format_model = WorkFormat(**work_format.model_dump())
        created_work_format = await self._uow.work_formats.add(work_format_model)

        self.get_work_format_by_name.cache_clear()

        return WorkFormatRead.model_validate(created_work_format)
