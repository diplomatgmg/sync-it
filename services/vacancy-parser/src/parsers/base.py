from abc import ABC, abstractmethod

from common.logger import get_logger


__all__ = ["BaseParser"]


logger = get_logger(__name__)


class BaseParser(ABC):
    def __init__(self) -> None:
        # Запоминаем fingerprints, которые получили на основе новых спарсенных вакансий, чтобы избежать конфликта с БД
        self.parsed_fingerprints: set[str] = set()

    @abstractmethod
    async def parse(self) -> None:
        """Основной метод парсинга каналов."""
