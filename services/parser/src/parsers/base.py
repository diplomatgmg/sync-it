from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

import httpx

from libs.logger import get_logger


__all__ = ["BaseParser"]


logger = get_logger(__name__)


class BaseParser(ABC):
    def __init__(self) -> None:
        self.http_client = httpx.AsyncClient()

    @abstractmethod
    async def parse(self) -> Sequence[int]:
        """Основной метод парсинга каналов"""

    @staticmethod
    @abstractmethod
    async def save_vacancies(vacancies: list[Any]) -> None:
        """Метод сохранения вакансий в базу"""
