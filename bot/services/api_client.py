import json
import typing as t

import aiohttp

from settings import CBR_URL, logger


async def get_current_exchange_rate() -> t.Dict[str, t.Any]:
    async with aiohttp.ClientSession() as session:
        # NOTE: Добавить кэширование
        async with session.get(CBR_URL) as resp:
            if resp.status == 200:
                raw_data: bytes = await resp.read()
                data: dict = json.loads(raw_data)
                return data
            else:
                logger.error(f'Ошибка при обращении к сервису {CBR_URL}: status_code={resp.status}, data={resp.text}')
                raise Exception('')
