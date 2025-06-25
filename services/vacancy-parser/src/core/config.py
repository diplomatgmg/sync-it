from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["service_config"]


class ServiceConfig(BaseSettings):
    db_schema: str = "vacancy_parser"

    host: str
    port: int = Field(ge=1, le=65535)

    hh_client_id: str
    hh_client_secret: str
    hh_access_token: str
    hh_email: str
    hh_app_name: str

    telegram_api_url: str

    model_config = SettingsConfigDict(env_prefix="VACANCY_PARSER_")


service_config = ServiceConfig()
