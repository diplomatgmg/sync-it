from typing import TYPE_CHECKING

from clients.head_hunter import head_hunter_client
from common.logger import get_logger
from parsers.base import BaseParser
from schemas.vacancy import HeadHunterVacancyCreate
from utils import clear_html, generate_fingerprint, generate_hash


__all__ = ["HeadHunterParser"]

if TYPE_CHECKING:
    from services import HeadHunterVacancyService

logger = get_logger(__name__)


class HeadHunterParser(BaseParser["HeadHunterVacancyService"]):
    def __init__(self, service: "HeadHunterVacancyService") -> None:
        super().__init__(service)
        self.service = service

    async def parse(self) -> None:
        logger.info("Starting HeadHunter parser")

        newest_vacancy_ids = await head_hunter_client.get_newest_vacancy_ids()
        vacancy_hashes = [generate_hash(vacancy_id) for vacancy_id in newest_vacancy_ids]
        existing_hashes = await self.service.get_existing_hashes(vacancy_hashes)

        new_vacancies_ids = [v_id for v_id in newest_vacancy_ids if generate_hash(v_id) not in existing_hashes]
        logger.info("Found %s new vacancies", len(new_vacancies_ids))

        vacancies: list[HeadHunterVacancyCreate] = []

        for vacancy_id in new_vacancies_ids[:50]:
            try:
                vacancy = await head_hunter_client.get_vacancy_by_id(vacancy_id)
            except Exception as e:
                logger.exception("Error processing vacancy with id %s", vacancy_id, exc_info=e)
                continue

            if not vacancy:
                logger.info("Skipping with id %s", vacancy_id)
                continue

            vacancy_description = clear_html(vacancy.description)

            fingerprint = generate_fingerprint(vacancy_description)
            duplicate = await self.service.find_duplicate_vacancy_by_fingerprint(fingerprint)
            if duplicate:
                logger.info(
                    "Found duplicate vacancy with similarity %s%%. New vacancy link: %s, Existing vacancy link: %s, ",
                    await self.service.get_similarity_score(fingerprint, duplicate.fingerprint),
                    vacancy.alternate_url,
                    duplicate.link,
                )
                await self.service.update_vacancy_published_at(duplicate.hash, vacancy.published_at)
                continue

            vacancy_create = HeadHunterVacancyCreate(
                fingerprint=fingerprint,
                vacancy_id=vacancy.id,
                link=vacancy.alternate_url,
                employer=vacancy.employer.name,
                name=vacancy.name,
                description=clear_html(vacancy.description),
                salary=vacancy.salary.humanize() if vacancy.salary else None,
                experience=vacancy.experience.name,
                schedule=vacancy.schedule.name,
                employment=vacancy.employment.name,
                work_formats=[wf.name for wf in vacancy.work_format],
                key_skills=[ks.name for ks in vacancy.key_skills],
                published_at=vacancy.published_at,
            )

            vacancies.append(vacancy_create)

        for new_vacancy in vacancies:
            await self.service.add_vacancy(new_vacancy)
            logger.info("Added vacancy %s", new_vacancy.link)
