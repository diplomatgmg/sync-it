import asyncio

from common.logger import get_logger
import uvloop


logger = get_logger(__name__)


async def main() -> None:
    await asyncio.sleep(1)
    logger.info("Starting service")


if __name__ == "__main__":
    uvloop.run(main())
