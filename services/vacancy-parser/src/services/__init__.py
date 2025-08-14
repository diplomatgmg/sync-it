# isort: off
from services.vacancy.vacancy import VacancyService
# isort: on

from services.vacancy.head_hunter import HeadHunterVacancyService
from services.vacancy.telegram import TelegramVacancyService


__all__ = [
    "HeadHunterVacancyService",
    "TelegramVacancyService",
    "VacancyService",
]
