from collections.abc import Sequence

from database.models import WorkFormat
from database.models.enums import WorkFormatEnum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["WorkFormatService"]


class WorkFormatService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_work_formats(self) -> Sequence[WorkFormat]:
        stmt = select(WorkFormat)
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def add_work_format(self, work_format: WorkFormatEnum) -> WorkFormat:
        work_format_model = WorkFormat(name=work_format)

        self.session.add(work_format_model)
        await self.session.commit()
        await self.session.refresh(work_format_model)

        return work_format_model
