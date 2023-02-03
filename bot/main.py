import asyncio

from aiogram import Bot, Dispatcher

from handlers.commands import register_common_handlers, set_commands
from handlers.notifications import register_notification_handlers
from services.utils import get_list_currencies
from settings.core import API_TOKEN, logger, storage
from settings.db import async_session, init_models


async def main():
    await init_models()
    bot = Bot(token=API_TOKEN)
    bot['db'] = async_session
    dp = Dispatcher(bot, storage=storage)
    all_currencies = await get_list_currencies()
    register_common_handlers(dp, data={'all_currencies': all_currencies})
    register_notification_handlers(dp)
    await set_commands(bot)

    # scheduler.add_job(jobs.check_current_exchange_rate, trigger='interval', seconds=10, kwargs={'bot': bot})
    # scheduler.start()
    # register_callbacks(dp)
    # await set_bot_commands(bot)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as e:
        logger.error(f'Bot stopped! {e}')
