import httpx

from libs.logger import get_logger


__all__ = ["validate_health_response"]


logger = get_logger(__name__)


def validate_health_response(response: httpx.Response) -> None:
    if response.status_code != httpx.codes.OK or "Telegram News – Telegram" not in response.text:  # noqa: RUF001
        logger.error("Unexpected healthcheck response: %s", response.text)
        raise ValueError("Unexpected healthcheck response")
