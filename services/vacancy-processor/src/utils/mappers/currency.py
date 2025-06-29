from common.logger import get_logger
from database.models.enums import CurrencyEnum


__all__ = ["map_to_currency_enum"]


logger = get_logger(__name__)


def map_to_currency_enum(currency: str) -> CurrencyEnum | None:
    currency = currency.lower().strip()

    for currency_enum, aliases in currency_map.items():
        if currency in aliases:
            return currency_enum

    return None


currency_map = {
    CurrencyEnum.RUB: ("rub",),
    CurrencyEnum.USD: ("usd",),
    CurrencyEnum.EUR: ("eur",),
}
