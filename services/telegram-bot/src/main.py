from common.logger import get_logger


logger = get_logger(__name__)


def main() -> None:
    logger.info("Hello from Telegram Bot Service")


if __name__ == "__main__":
    main()
