from pydantic_settings import BaseSettings, SettingsConfigDict
from schemas import TelegramChannelUrl
from pydantic import Field

__all__ = ["parser_config"]


class ParserConfig(BaseSettings):
    host: str
    port: int = Field(ge=1, le=65535)

    hh_client_id: str
    hh_client_secret: str
    hh_access_token: str
    hh_email: str
    hh_app_name: str

    telegram_channel_links: list[TelegramChannelUrl]  # https://t.me/s/<channel_name>

    telegram_api_url: str

    model_config = SettingsConfigDict(env_prefix="VACANCY_PARSER_")


parser_config = ParserConfig()
