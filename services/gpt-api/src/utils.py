from libs.logger import get_logger


__all__ = ["validate_health_response"]


logger = get_logger(__name__)


def validate_health_response(response_text: str) -> None:
    expected_responses = {"healthy", "healthy.", "healthy!"}

    if response_text.lower() not in expected_responses:
        error_msg = f'Unexpected healthcheck response: "{response_text}"'
        logger.error(error_msg)
        raise ValueError(error_msg)
