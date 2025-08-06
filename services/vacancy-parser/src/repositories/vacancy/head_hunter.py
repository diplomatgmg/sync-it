from datetime import datetime

from database.models.enums import SourceEnum
from database.models.vacancy import HeadHunterVacancy
from repositories.vacancy.vacancy import VacancyRepository
from sqlalchemy import select
from utils import generate_hash


__all__ = ["HeadHunterVacancyRepository"]


class HeadHunterVacancyRepository(VacancyRepository):
    source = SourceEnum.HEAD_HUNTER
    model = HeadHunterVacancy

    async def get_vacancy_by_id(self, vacancy_id: int) -> HeadHunterVacancy | None:
        stmt = select(self.model).where(self.model.vacancy_id == vacancy_id)
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def prepare_instance(
        self,
        *,
        fingerprint: str,
        vacancy_id: int,
        link: str,
        data: str,
        published_at: datetime,
    ) -> HeadHunterVacancy:
        hash_value = generate_hash(str(vacancy_id))
        source_id = await self.get_source_id()

        return self.model(
            hash=hash_value,
            source_id=source_id,
            fingerprint=fingerprint,
            vacancy_id=vacancy_id,
            link=link,
            data=data,
            published_at=published_at,
        )
