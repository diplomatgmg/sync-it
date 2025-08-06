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

    def humanize(self) -> str:
        match self:
            case self.RUR:
                return "RUB"
            case self.BYR:
                return "BYN"

        return str(self.value)


class SalaryMode(StrEnum):
    MONTH = "MONTH"

    def humanize(self) -> str | None:
        match self:
            case self.MONTH:
                return "в месяц"

        return None
