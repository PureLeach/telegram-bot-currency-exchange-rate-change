import json
import typing as t

import aiohttp

from settings import CBR_URL


async def get_current_exchange_rate() -> t.Dict[str, t.Any]:
    async with aiohttp.ClientSession() as session:
        # NOTE: Добавить кэширование
        async with session.get(CBR_URL) as resp:
            if resp.status == 200:
                raw_data: bytes = await resp.read()
                data: dict = json.loads(raw_data)
                return data
            else:
                # NOTE LOG
                raise Exception('')
