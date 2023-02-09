import typing as t

from aiocache import cached
from flag import flag

from controllers import CurrencyController, UserController
from settings.core import CACHE_TTL


@cached(ttl=CACHE_TTL)
async def get_list_currencies(emoji=False) -> t.List[str]:
    """Returns a list of all currencies from the database in uppercase or emoji flags"""
    all_currencies = await CurrencyController.get_all_currencies()
    if emoji:
        return [flag(currency.char_code[:2]) for currency in all_currencies]
    return [currency.char_code.upper() for currency in all_currencies]


@cached(ttl=CACHE_TTL)
async def get_dict_flag_currencies() -> t.Dict[str, str]:
    """Returns a dictionary of all currencies from the database in the form of key=char_code, value=emoji_flag"""
    all_currencies = await CurrencyController.get_all_currencies()
    return {flag(currency.char_code[:2]): currency.char_code for currency in all_currencies}


async def get_user_currency_data(user_id: int, action: str) -> str:
    """Generate information on which currencies the user can subscribe or unsubscribe"""
    currencies = await UserController.get_users_currencies(user_id)
    if action == 'subscribe':
        all_currencies = await CurrencyController.get_all_currencies()
        currencies = [currency.char_code for currency in all_currencies if currency.char_code not in currencies]
    data = ''
    for currency in currencies:
        data += f'{flag(currency[:2])} - /{currency.upper()}\n'
    return data
