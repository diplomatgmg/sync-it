import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from schemas import TelegramChannelUrl


__all__ = ["parser_config"]


class ParserConfig(BaseSettings):
    hh_client_id: str
    hh_client_secret: str
    hh_access_token: str
    hh_email: str
    hh_app_name: str

    telegram_channel_links: list[TelegramChannelUrl]  # https://t.me/s/<channel_name>

    model_config = SettingsConfigDict(env_prefix="PARSER_")

    @property
    def telegram_parser_service_url(self) -> str:
        api_port = os.getenv("TELEGRAM_PARSER_API_PORT")
        if api_port is None:
            raise ValueError("TELEGRAM_PARSER_API_PORT is not set")

        return f"http://telegram-parser-api:{api_port}"


parser_config = ParserConfig()
