import re

from pydantic import BaseModel, HttpUrl, UrlConstraints
from serializers import VacancySerializer


__all__ = [
    "HealthResponse",
    "TelegramChannelMessage",
    "TelegramChannelMessagesResponse",
    "TelegramChannelUrl",
    "VacancyResponse",
]


class TelegramChannelUrl(HttpUrl):
    """
    A custom URL type for validating Telegram channel links.

    ex. valid URL: https://t.me/s/<channel_name>
    """

    _constraints = UrlConstraints(allowed_schemes=["https"])

    def __init__(self, url: str) -> None:
        super().__init__(url)
        self._validate_url()

    @property
    def channel_username(self) -> str:
        return self.path.split("/")[-1]  # type: ignore[union-attr]

    def _validate_url(self) -> None:
        self._validate_host()
        self._validate_path_structure()

    def _validate_host(self) -> None:
        if self.host != "t.me":
            raise ValueError(f"Invalid Telegram URL host '{self.host}'. Host must be 't.me'")

    def _validate_path_structure(self) -> None:
        """Ensure path starts with '/s/' and has username after."""
        path_pattern = r"^/s/(?P<username>[a-zA-Z0-9_]{5,32})$"  # ex.: /s/MyChannel_0123
        match = re.match(path_pattern, self.path or "")
        if not match:
            raise ValueError(
                f"Invalid Telegram channel URL: path '{self.path}' must be in format '/s/<channel_name>' "
                "with username 5-32 chars, letters, digits, underscore only"
            )


class TelegramChannelMessage(BaseModel):
    message_id: int
    text: str


class TelegramChannelMessagesResponse(BaseModel):
    messages: list[TelegramChannelMessage]


class HealthResponse(BaseModel):
    status: str


class VacancyResponse(BaseModel):
    vacancies: list[VacancySerializer]
