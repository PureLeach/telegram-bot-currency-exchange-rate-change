import json

from aiocache import cached
from aiohttp import ClientSession
from flag import flag

from controllers import CurrencyController, UserController
from models.exceptions import CurrencyException
from schemas.exchange_rate import SchemaBodyCurrentExchangeRate
from services.exceptions import CBRException
from settings.core import CACHE_TTL, CBR_URL, logger


async def get_user_currency_data(user_id: int, action: str) -> str:
    """
    Generate information on which currencies the user can subscribe or unsubscribe
    """
    currencies = await UserController.get_users_currencies(user_id)
    if action == 'subscribe':
        all_currencies = await CurrencyController.get_all_currencies()
        currencies = [currency.char_code for currency in all_currencies if currency.char_code not in currencies]
    data = ''
    for currency in currencies:
        data += f'{flag(currency[:2])} - /{currency.upper()}\n'
    return data


async def collect_users_exchange_rates(raw_data: bytes, currencies: list) -> str:
    """
    Collect information about those exchange rates
    to which the user is subscribed
    """
    data = json.loads(raw_data)
    load_schema = SchemaBodyCurrentExchangeRate(**data)
    users_exchange_rates = ''
    for currency in currencies:
        valute = getattr(load_schema.valute, currency)
        users_exchange_rates += f'{flag(valute.char_code[:2])} {valute.char_code}: {valute.value}\n'
    return users_exchange_rates


@cached(ttl=CACHE_TTL)
async def get_current_exchange_rate_for_user(user_id: int) -> str:
    """Request information about the current exchange rate and generate data for the user"""
    currencies = await UserController.get_users_currencies(user_id)
    if not currencies:
        raise CurrencyException('User does not have subscriptions to currencies')
    async with ClientSession() as session:
        async with session.get(CBR_URL, timeout=10) as response:
            if response.status == 200:
                raw_data = await response.read()
                return await collect_users_exchange_rates(raw_data, currencies)
            else:
                logger.error(
                    f'Ошибка при обращении к сервису {CBR_URL}: status_code={response.status}, data={response.text}'
                )
                raise CBRException(f'Error when requesting data: status_code={response.status}, data={response.text}')


async def get_current_exchange_rate() -> SchemaBodyCurrentExchangeRate:
    """Request information about the current exchange rate without cache"""
    async with ClientSession() as session:
        async with session.get(CBR_URL, timeout=10) as response:
            if response.status == 200:
                raw_data = await response.read()
                data = json.loads(raw_data)
                return SchemaBodyCurrentExchangeRate(**data)
            else:
                logger.error(
                    f'Ошибка при обращении к сервису {CBR_URL}: status_code={response.status}, data={response.text}'
                )
                raise CBRException(f'Error when requesting data: status_code={response.status}, data={response.text}')
