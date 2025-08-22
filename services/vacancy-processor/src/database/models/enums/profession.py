from database.models.enums import BaseAliasEnum


__all__ = ["ProfessionEnum"]


class ProfessionEnum(BaseAliasEnum):
    __validate_ordering__ = True

    UNKNOWN = "Неизвестно"

    BACKEND = "Backend developer", ("java-разработчик", "back-end developer", "python-разработчик")
    DEVOPS = "DevOps"
    DATA_ENGINEER = "Data Engineer"
    DATA_SCIENCE = "Data Science"
    FRONTEND = "Frontend developer"
    FULLSTACK = "Fullstack developer"
    QA_ENGINEER = "QA Engineer", ("fullstack qa", "qa automation engineer")
    TECH_LEAD = "Tech Lead"
    UX_UX_DESIGNER = "UX/UI-дизайнер"
