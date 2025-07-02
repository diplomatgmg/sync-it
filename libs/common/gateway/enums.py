from enum import StrEnum


__all__ = ["ServiceEnum"]


class ServiceEnum(StrEnum):
    TELEGRAM_API = "telegram-api"
    GPT_API = "gpt-api"
    VACANCY_PARSER = "vacancy-parser"
    VACANCY_PROCESSOR = "vacancy-processor"
