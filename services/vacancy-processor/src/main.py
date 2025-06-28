import asyncio

from common.logger import get_logger
from seeds import seed_models
from services.http import fetch_gpt_completion, fetch_new_vacancies
from services.prompter import make_prompt
from utils.normalizers.vormalize_prompted_vacancy import normalize_prompted_vacancy
import uvloop


logger = get_logger(__name__)


async def main() -> None:
    await seed_models()

    vacancies = await fetch_new_vacancies()

    logger.info("Got %s vacancies", len(vacancies))

    prompts = [make_prompt(vacancy.data) for vacancy in vacancies]
    tasks = [fetch_gpt_completion(prompt) for prompt in prompts]
    data = await asyncio.gather(*tasks)

    for vacancy, item in zip(vacancies, data, strict=True):
        logger.info("Processing vacancy: %s", vacancy.link)
        normalize_prompted_vacancy(item)


if __name__ == "__main__":
    uvloop.run(main())
