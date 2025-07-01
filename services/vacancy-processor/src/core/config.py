from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["service_config"]


class ServiceConfig(BaseSettings):
    db_schema: str = "vacancy_processor"

    model_config = SettingsConfigDict(env_prefix="VACANCY_PROCESSOR_")


service_config = ServiceConfig()
