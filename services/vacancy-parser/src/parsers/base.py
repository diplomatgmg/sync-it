from abc import ABC, abstractmethod

from common.logger import get_logger


__all__ = ["BaseParser"]


logger = get_logger(__name__)


class BaseParser[ServiceType](ABC):
    def __init__(self, service: ServiceType) -> None:
        self.service = service
        self._processed_fingerprints: set[str] = set()

    @abstractmethod
    async def parse(self) -> None:
        """Основной метод парсинга каналов."""
