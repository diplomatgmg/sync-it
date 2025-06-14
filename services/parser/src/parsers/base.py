from abc import ABC, abstractmethod
from collections.abc import Sequence

from libs.logger import get_logger


__all__ = ["BaseParser"]


logger = get_logger(__name__)


class BaseParser(ABC):
    @abstractmethod
    async def parse(self) -> Sequence[int]:
        pass
