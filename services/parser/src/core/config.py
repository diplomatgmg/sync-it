from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["parser_config"]


class ParserConfig(BaseSettings):
    hh_client_id: str
    hh_client_secret: str
    hh_access_token: str
    hh_email: str
    hh_app_name: str

    model_config = SettingsConfigDict(env_prefix="PARSER_")


parser_config = ParserConfig()
