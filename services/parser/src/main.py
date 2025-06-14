import asyncio

from parsers.hh import HHParser
import uvloop

from libs.logger import get_logger


logger = get_logger(__name__)


async def main() -> None:
    logger.info("Hello from parser")

    parsers = [HHParser()]

    tasks = [asyncio.create_task(parser.parse()) for parser in parsers]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    uvloop.run(main())
