# isort: off
from services.vacancy.base import BaseVacancyService
from services.vacancy.vacancy import VacancyService
# isort: on

from services.vacancy.head_hunter import HeadHunterVacancyService
from services.vacancy.telegram import TelegramVacancyService


__all__ = [
    "BaseVacancyService",
    "HeadHunterVacancyService",
    "TelegramVacancyService",
    "VacancyService",
]
