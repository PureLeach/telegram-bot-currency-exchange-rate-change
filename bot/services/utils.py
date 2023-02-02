import typing as t

from aiocache import cached
from flag import flag

from controllers import CurrencyController
from settings.core import CACHE_TTL


@cached(ttl=CACHE_TTL)
async def get_list_currencies() -> t.List[str]:
    """Возвращает список всех валют из БД в верхнем регистре"""
    all_currencies = await CurrencyController.get_all_currencies()
    return [currency.char_code.upper() for currency in all_currencies]


@cached(ttl=CACHE_TTL)
async def get_list_flag_currencies() -> t.List[str]:
    """Возвращает список всех валют из БД в виде эмодзи флагов"""
    all_currencies = await CurrencyController.get_all_currencies()
    return [flag(currency.char_code[:2]) for currency in all_currencies]


@cached(ttl=CACHE_TTL)
async def get_dict_flag_currencies() -> t.Dict[str, str]:
    """Возвращает словарь всех валют из БД в виде key=char code, value=эмодзи флаг"""
    all_currencies = await CurrencyController.get_all_currencies()
    return {flag(currency.char_code[:2]): currency.char_code for currency in all_currencies}
