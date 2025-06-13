import logging
import time

from core.config import parser_config


logger = logging.getLogger(__name__)


def main() -> None:
    logger.info(parser_config.model_config)
    print(parser_config.model_config)
    time.sleep(10000)


if __name__ == "__main__":
    main()
