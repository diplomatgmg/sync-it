from collections.abc import Sequence

from database.models import WorkFormat
from database.models.enums import WorkFormatEnum
from repositories import WorkFormatRepository


__all__ = ["WorkFormatService"]


class WorkFormatService:
    """Сервис для бизнес-операций, связанных с форматами работы."""

    def __init__(self, repo: WorkFormatRepository) -> None:
        self.repo = repo

    async def get_work_format_by_name(self, name: WorkFormatEnum) -> WorkFormat | None:
        return await self.repo.get_by_name(name)

    async def get_work_formats(self) -> Sequence[WorkFormat]:
        return await self.repo.get_all()

    async def add_work_format(self, work_format: WorkFormatEnum) -> None:
        """Создает и добавляет формат работы в сессию (без коммита)."""
        work_format_model = WorkFormat(name=work_format)
        self.repo.add(work_format_model)
