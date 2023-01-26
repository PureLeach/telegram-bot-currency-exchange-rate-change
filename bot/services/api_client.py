import json

import aiohttp

from schemas.exchange_rate import SchemaBodyCurrentExchangeRate
from settings import CBR_URL, logger


class ExchangeRateClient:
    @staticmethod
    async def collect_users_exchange_rates(raw_data: bytes) -> str:
        """
        Collect information about those exchange rates
        to which the user is subscribed
        """
        # NOTE Добавить эмодзи
        data = json.loads(raw_data)
        load_schema = SchemaBodyCurrentExchangeRate(**data)
        # NOTE Добавить таблицу курсов валют пользователя
        currencies = ['usd', 'eur']
        users_exchange_rates = ''
        for currency in currencies:
            valute = getattr(load_schema.valute, currency)
            users_exchange_rates += f'{valute.char_code}: {valute.value}\n'
        return users_exchange_rates

    @staticmethod
    async def get_current_exchange_rate() -> str:
        async with aiohttp.ClientSession() as session:
            # NOTE: Добавить кэширование
            async with session.get(CBR_URL) as resp:
                if resp.status == 200:
                    raw_data = await resp.read()
                    return await ExchangeRateClient.collect_users_exchange_rates(raw_data)
                else:
                    logger.error(
                        f'Ошибка при обращении к сервису {CBR_URL}: status_code={resp.status}, data={resp.text}'
                    )
                    raise Exception('')
