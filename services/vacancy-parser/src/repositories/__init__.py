# isort: off
from repositories.vacancy.vacancy import VacancyRepository
# isort: on

from repositories.vacancy.head_hunter import HeadHunterVacancyRepository
from repositories.vacancy.telegram import TelegramVacancyRepository


__all__ = [
    "HeadHunterVacancyRepository",
    "TelegramVacancyRepository",
    "VacancyRepository",
]
