import json
from decimal import Decimal

from aiohttp import ClientSession
from flag import flag

from controllers import UserController
from models.exceptions import CurrencyException
from schemas.exchange_rate import SchemaBodyCurrentExchangeRate
from services.exceptions import CBRServiceUnavailable
from settings.core import CACHE_TTL, CBR_URL, cache, logger


async def get_data_current_exchange_rate(actual=False):
    """
    Request information about the current exchange rate.
    If argument actual=True is passed, return uncached data
    """
    try:
        if not actual and (schema := await cache.get('current_exchange_rate')):
            return schema
        async with ClientSession() as session:
            async with session.get(CBR_URL, timeout=10) as response:
                raw_data = await response.read()
                data = json.loads(raw_data)
                schema = SchemaBodyCurrentExchangeRate(**data)
                await cache.set('current_exchange_rate', schema, ttl=CACHE_TTL)
                return schema
    except Exception as e:
        logger.error(f'Error when receiving data from CBR service: error={e}')
        raise CBRServiceUnavailable


async def get_current_exchange_rate_value(currency_char: str) -> Decimal:
    """Get the current currency value by code"""
    current_exchange_rate = await get_data_current_exchange_rate(actual=True)
    current_value = Decimal(getattr(current_exchange_rate.valute, currency_char).value).quantize(Decimal('1.0000'))
    return current_value


async def get_data_current_exchange_rate_for_user(user_id: int) -> str:
    """Request information about the current exchange rate and generate data for the user"""
    currencies = await UserController.get_users_currencies(user_id)
    if not currencies:
        raise CurrencyException('User does not have subscriptions to currencies')
    current_exchange_rate = await get_data_current_exchange_rate()
    return await collect_users_exchange_rates(current_exchange_rate, currencies)


async def collect_users_exchange_rates(current_exchange_rate: SchemaBodyCurrentExchangeRate, currencies: list) -> str:
    """Collect information about those exchange rates to which the user is subscribed"""
    users_exchange_rates = ''
    for currency in currencies:
        valute = getattr(current_exchange_rate.valute, currency)
        users_exchange_rates += f'{flag(valute.char_code[:2])} {valute.char_code}: {valute.value}\n'
    return users_exchange_rates
