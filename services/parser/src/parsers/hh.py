from collections.abc import Sequence

from parsers.base import BaseParser

from libs.logger import get_logger


__all__ = ["HHParser"]


logger = get_logger(__name__)


class HHParser(BaseParser):
    async def parse(self) -> Sequence[int]:
        logger.info("Start parsing %s", self.__class__.__name__)
        return [1, 2, 3]
