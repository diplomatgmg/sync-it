from services.http.gpt import fetch_gpt_completion
from services.http.vacancy import fetch_new_vacancies, send_delete_request_vacancy


__all__ = [
    "fetch_gpt_completion",
    "fetch_new_vacancies",
    "send_delete_request_vacancy",
]
