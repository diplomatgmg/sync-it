from database.services.telegram_vacancy import TelegramVacancyService
from parsers import TelegramParser
import uvloop

from libs.database.engine import get_async_session
from libs.logger import get_logger


logger = get_logger(__name__)


async def main() -> None:
    pass


if __name__ == "__main__":
    uvloop.run(main())
