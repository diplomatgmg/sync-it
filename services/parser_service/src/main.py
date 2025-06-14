import asyncio

from logger import get_logger
from parsers.hh import HHParser
import uvloop

logger = get_logger(__name__)


async def main() -> None:
    parsers = [HHParser()]

    tasks = [asyncio.create_task(parser.parse()) for parser in parsers]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    uvloop.run(main())
