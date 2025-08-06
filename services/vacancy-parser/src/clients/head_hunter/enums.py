from enum import StrEnum


__all__ = [
    "SalaryCurrency",
    "SalaryMode",
]


class SalaryCurrency(StrEnum):
    RUR = "RUR"
    EUR = "EUR"
    USD = "USD"
    KZT = "KZT"
    BYR = "BYR"
    GEL = "GEL"
    UZS = "UZS"
    KGS = "KGS"


class SalaryMode(StrEnum):
    MONTH = "MONTH"

    def humanize(self) -> str | None:
        match self:
            case self.MONTH:
                return "в месяц"

        return None
