from abc import ABC, abstractmethod
from typing import TypeVar

from common.logger import get_logger
from database.models.vacancy import BaseVacancy


__all__ = ["BaseParser"]


logger = get_logger(__name__)

VacancyType = TypeVar("VacancyType", bound=BaseVacancy)


class BaseParser(ABC):
    # Батч для сохранения вакансий
    BATCH_SIZE = 50

    def __init__(self) -> None:
        # Запоминаем fingerprints, которые получили на основе новых спарсенных вакансий, чтобы избежать конфликта с БД
        self.parsed_fingerprints: set[str] = set()

    @abstractmethod
    async def parse(self) -> None:
        """Основной метод парсинга каналов."""

    async def save_vacancies(self, vacancies: list[VacancyType]) -> None:
        """Сохраняет вакансии."""
        if not vacancies:
            logger.info("No new vacancies to save for parser '%s'", self.__class__.__name__)
            return

        saved_count = await self.service.bulk_create(vacancies)  # type: ignore[attr-defined]
        logger.info("Saved %s new vacancies", saved_count)
