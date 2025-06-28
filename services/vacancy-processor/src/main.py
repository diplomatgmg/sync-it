from common.logger import get_logger
from seeds import seed_models
from services.vacancy import VacancyProcessorService
import uvloop


logger = get_logger(__name__)


async def main() -> None:
    await seed_models()

    service = VacancyProcessorService()
    await service.start()


if __name__ == "__main__":
    uvloop.run(main())
