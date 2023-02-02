import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from handlers.commands import register_commands
from handlers.notifications import register_handlers_notification
from services.utils import get_list_currencies
from settings.core import API_TOKEN, logger, storage
from settings.db import async_session, init_models


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Заказать напитки'),
        BotCommand(command='/cancel', description='Отменить текущее действие'),
    ]
    await bot.set_my_commands(commands)


async def main():
    await init_models()
    bot = Bot(token=API_TOKEN)
    bot['db'] = async_session
    dp = Dispatcher(bot, storage=storage)
    all_currencies = await get_list_currencies()
    register_commands(dp, data={'all_currencies': all_currencies})
    register_handlers_notification(dp)
    # Установка команд бота
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
