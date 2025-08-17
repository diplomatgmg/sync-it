from abc import ABC, abstractmethod

from common.logger import get_logger
from unitofwork import UnitOfWork


__all__ = ["BaseParser"]


logger = get_logger(__name__)


class BaseParser[ServiceType](ABC):
    def __init__(self, uow: UnitOfWork, service: ServiceType) -> None:
        self.uow = uow
        self.service = service

    @abstractmethod
    async def parse(self) -> None:
        """Основной метод парсинга каналов."""
