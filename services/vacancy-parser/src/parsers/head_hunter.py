from typing import TYPE_CHECKING

from clients.head_hunter import head_hunter_client
from common.logger import get_logger
from parsers.base import BaseParser
from schemas.vacancy import HeadHunterVacancyCreate
from unitofwork import UnitOfWork
from utils import clear_html, generate_fingerprint, generate_hash


__all__ = ["HeadHunterParser"]

if TYPE_CHECKING:
    from services import HeadHunterVacancyService


logger = get_logger(__name__)


class HeadHunterParser(BaseParser["HeadHunterVacancyService"]):
    def __init__(self, uow: UnitOfWork, service: "HeadHunterVacancyService") -> None:
        super().__init__(uow, service)
        self.service = service

    async def parse(self) -> None:
        logger.info("Starting HeadHunter parser")

        newest_vacancy_ids = await head_hunter_client.get_newest_vacancy_ids()
        vacancy_hashes = [generate_hash(vacancy_id) for vacancy_id in newest_vacancy_ids]
        existing_hashes = await self.service.get_existing_hashes(vacancy_hashes)

        new_vacancies_ids = [v_id for v_id in newest_vacancy_ids if generate_hash(v_id) not in existing_hashes]
        logger.info("Found %s new vacancies", len(new_vacancies_ids))

        for vacancy_id in new_vacancies_ids:
            try:
                vacancy_detail = await head_hunter_client.get_vacancy_by_id(vacancy_id)
            except Exception as e:
                logger.exception("Error processing vacancy with id %s", vacancy_id, exc_info=e)
                continue

            if not vacancy_detail:
                logger.info("Skipping with id %s", vacancy_id)
                continue

            vacancy_description = clear_html(vacancy_detail.description)

            fingerprint = generate_fingerprint(vacancy_description)
            duplicate = await self.service.find_duplicate_vacancy_by_fingerprint(fingerprint)
            if duplicate:
                logger.info(
                    "Found duplicate vacancy. New vacancy link: %s, Existing vacancy link: %s",
                    vacancy_detail.alternate_url,
                    duplicate.link,
                )
                await self.service.update_vacancy_published_at(duplicate.hash, vacancy_detail.published_at)
                continue

            vacancy = HeadHunterVacancyCreate(
                fingerprint=fingerprint,
                vacancy_id=vacancy_detail.id,
                link=vacancy_detail.alternate_url,
                employer=vacancy_detail.employer.name,
                name=vacancy_detail.name,
                description=clear_html(vacancy_detail.description),
                salary=vacancy_detail.salary.humanize() if vacancy_detail.salary else None,
                experience=vacancy_detail.experience.name,
                schedule=vacancy_detail.schedule.name,
                work_formats=[wf.name for wf in vacancy_detail.work_format],
                key_skills=[ks.name for ks in vacancy_detail.key_skills],
                published_at=vacancy_detail.published_at,
            )

            await self.service.add_vacancy(vacancy)
            await self.uow.commit()
            logger.info("Added vacancy %s", vacancy.link)
