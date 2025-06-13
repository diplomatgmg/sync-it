from collections.abc import Sequence

from logger import get_logger
from parsers.base import BaseParser


__all__ = ["HHParser"]


logger = get_logger(__name__)


class HHParser(BaseParser):
    async def parse(self) -> Sequence[int]:
        logger.info("Start parsing %s", self.__class__.__name__)
        return [1, 2, 3]
