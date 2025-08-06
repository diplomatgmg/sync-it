from datetime import datetime

from database.models.vacancy import HeadHunterVacancy
from repositories.vacancy import HeadHunterVacancyRepository
from services.vacancy import BaseVacancyService


__all__ = ["HeadHunterVacancyService"]


class HeadHunterVacancyService(BaseVacancyService[HeadHunterVacancyRepository]):
    """Сервис для бизнес-логики, связанной с вакансиями из HeadHunter."""

    async def get_vacancy_by_id(self, vacancy_id: int) -> HeadHunterVacancy | None:
        return await self._repo.get_vacancy_by_id(vacancy_id)

    async def prepare_instance(
        self,
        *,
        fingerprint: str,
        vacancy_id: int,
        link: str,
        name: str,
        description: str,
        salary: str | None,
        experience: str,
        employment: str,
        schedule: str,
        work_formats: list[str],
        published_at: datetime,
    ) -> HeadHunterVacancy:
        text_parts: list[str] = [f"Вакансия: {name}"]
        if salary:
            text_parts.append(f"Зарплата: {salary}")
        text_parts.extend((f"Опыт: {experience}", f"Занятость: {employment}", f"График работы: {schedule}"))
        if work_formats:
            text_parts.append(f"Формат работы: {' '.join(work_formats)}")
        text_parts.append(f"Описание: \n{description}")

        data = "\n".join(text_parts)

        return await self._repo.prepare_instance(
            fingerprint=fingerprint,
            vacancy_id=vacancy_id,
            link=link,
            data=data,
            published_at=published_at,
        )
