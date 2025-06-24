from common.logger import get_logger
from services.vacancy import get_newest_vacancies
import uvloop


logger = get_logger(__name__)


async def main() -> None:
    vacancies = await get_newest_vacancies()
    logger.info("Got %s vacancies", len(vacancies))


if __name__ == "__main__":
    uvloop.run(main())
