# ruff: noqa: E501

from database.models.enums import BaseAliasEnum


__all__ = ["ProfessionEnum"]


# fmt: off
class ProfessionEnum(BaseAliasEnum):
    __validate_ordering__ = True

    UNKNOWN = "Неизвестно"

    ANALYST = "Аналитик", ("системный аналитик",)
    BACKEND = "Backend developer", ("java-разработчик", "back-end developer", "python-разработчик", "backend-разработчик", "backend разработчик")
    DATA_ENGINEER = "Data Engineer"
    DATA_SCIENCE = "Data Science", ("data scientist",)
    DEVOPS = "DevOps", ("devops инженер", "devops-инженер", "devops engineer", "devops/mlops инженер")
    FRONTEND = "Frontend developer", ("frontend разработчик", "flutter-разработчик")
    FULLSTACK = "Fullstack developer", ("fullstack разработчик",)
    QA_ENGINEER = "QA Engineer", ("fullstack qa", "qa automation engineer", "тестировщик", "qa инженер")
    TECH_LEAD = "Tech Lead"
    UX_UX_DESIGNER = "UX/UI-дизайнер", ("ux/ui дизайнер",)
# fmt: on
