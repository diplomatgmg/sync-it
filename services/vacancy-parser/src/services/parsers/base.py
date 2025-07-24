from abc import ABC, abstractmethod
from typing import Any

from common.logger import get_logger


__all__ = ["BaseParser"]


logger = get_logger(__name__)


class BaseParser(ABC):
    @abstractmethod
    async def parse(self) -> None:
        """Основной метод парсинга каналов"""

    @abstractmethod
    async def save_vacancies(self, vacancies: list[Any]) -> None:
        """Метод сохранения вакансий в базу"""
