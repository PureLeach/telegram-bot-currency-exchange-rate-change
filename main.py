import asyncio

from aiogram import Bot, Dispatcher

from db.base import async_session, init_models
from handlers.commands import register_commands
from settings import API_TOKEN


async def main():
    await init_models()
    bot = Bot(token=API_TOKEN)
    bot['db'] = async_session
    dp = Dispatcher(bot)
    register_commands(dp)
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
        print(f'\033[31m e, { e }, {type(e)} \033[0m')
        # logging.error("Bot stopped!")
