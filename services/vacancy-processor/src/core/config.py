from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["service_config"]


class ServiceConfig(BaseSettings):
    db_schema: str = "vacancy_processor"

    vacancy_parser_url: str
    gpt_api_url: str

    model_config = SettingsConfigDict(env_prefix="VACANCY_PROCESSOR_")


service_config = ServiceConfig()
