import uvloop

from libs.logger import get_logger


logger = get_logger(__name__)


async def main() -> None:
    pass


if __name__ == "__main__":
    uvloop.run(main())
