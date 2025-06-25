import asyncio

from common.logger import get_logger
from services.http import fetch_gpt_completion, fetch_new_vacancies
from services.prompter import make_prompt
import uvloop


logger = get_logger(__name__)


async def main() -> None:
    vacancies = (await fetch_new_vacancies())[:10]

    logger.info("Got %s vacancies", len(vacancies))

    prompts = [make_prompt(vacancy.data) for vacancy in vacancies]
    tasks = [fetch_gpt_completion(prompt) for prompt in prompts]
    data = await asyncio.gather(*tasks)

    for _vacancy, _prompted in zip(vacancies, data, strict=True):
        logger.info("%s %s", _vacancy.link, _prompted[:200])


if __name__ == "__main__":
    uvloop.run(main())
