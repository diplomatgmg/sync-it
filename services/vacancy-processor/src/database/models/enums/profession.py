from database.models.enums import BaseAliasEnum


__all__ = ["ProfessionEnum"]


class ProfessionEnum(BaseAliasEnum):
    UNKNOWN = "Неизвестно"
    DEVOPS = "DevOps"
    BACKEND = "Backend developer"
    FRONTEND = "Frontend developer"
    FULLSTACK = "Fullstack developer"
    DATA_ENGINEER = "Data Engineer"
    DATA_SCIENCE = "Data Science"
    TECH_LEAD = "Tech Lead"
