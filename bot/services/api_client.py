import json

from aiohttp_client_cache import CachedSession

from controllers.user import UserController
from models.exceptions import CurrencyException
from schemas.exchange_rate import SchemaBodyCurrentExchangeRate
from services.exceptions import CBRException
from settings import CBR_URL, cache, logger


class ExchangeRateClient:
    @staticmethod
    async def collect_users_exchange_rates(raw_data: bytes, currencies: list) -> str:
        """
        Collect information about those exchange rates
        to which the user is subscribed
        """
        # NOTE Добавить эмодзи
        data = json.loads(raw_data)
        load_schema = SchemaBodyCurrentExchangeRate(**data)
        users_exchange_rates = ''
        for currency in currencies:
            valute = getattr(load_schema.valute, currency)
            users_exchange_rates += f'{valute.char_code}: {valute.value}\n'
        return users_exchange_rates

    @staticmethod
    async def get_current_exchange_rate(id: int) -> str:
        currencies = await UserController.get_users_currencies(id)
        if not currencies:
            raise CurrencyException('User does not have subscriptions to currencies')
        async with CachedSession(cache=cache) as session:
            async with session.get(CBR_URL, timeout=10) as response:
                if response.status == 200:
                    raw_data = await response.read()
                    return await ExchangeRateClient.collect_users_exchange_rates(raw_data, currencies)
                else:
                    logger.error(
                        f'Ошибка при обращении к сервису {CBR_URL}: status_code={response.status}, data={response.text}'
                    )
                    raise CBRException(
                        f'Error when requesting data: status_code={response.status}, data={response.text}'
                    )
