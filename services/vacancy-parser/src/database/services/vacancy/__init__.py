# isort: off
from database.services.vacancy.vacancy import VacancyService
from database.services.vacancy.telegram_vacancy import TelegramVacancyService
# isort: on

__all__ = [
    "TelegramVacancyService",
    "VacancyService",
]
