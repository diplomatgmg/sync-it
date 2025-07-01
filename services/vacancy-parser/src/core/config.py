from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["service_config"]


class ServiceConfig(BaseSettings):
    db_schema: str = "vacancy_parser"

    hh_client_id: str
    hh_client_secret: str
    hh_access_token: str
    hh_email: str
    hh_app_name: str

    model_config = SettingsConfigDict(env_prefix="VACANCY_PARSER_")


service_config = ServiceConfig()
