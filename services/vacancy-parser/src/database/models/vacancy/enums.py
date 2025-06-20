from enum import StrEnum


__all__ = ["VacancySource"]


class VacancySource(StrEnum):
    TELEGRAM = "telegram"
    HH = "hh"
