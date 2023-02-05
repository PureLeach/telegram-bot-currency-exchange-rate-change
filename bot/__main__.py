import asyncio

from aiogram import Bot, Dispatcher

from handlers.common import register_common_handlers, set_commands
from handlers.exchange_rate import register_exchange_rate_handlers
from handlers.notifications import register_notification_handlers
from jobs.periodic_tasks import check_current_exchange_rate
from middlewares.logger_middleware import LoggerMiddleware
from services.currencies import get_list_currencies
from settings.core import API_TOKEN, logger, storage
from settings.scheduler import JOB_INTERVAL, scheduler


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(LoggerMiddleware())
    register_common_handlers(dp)
    all_currencies = await get_list_currencies()
    register_exchange_rate_handlers(dp, data={'all_currencies': all_currencies})
    register_notification_handlers(dp)
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.add_job(
        check_current_exchange_rate,
        trigger='interval',
        minutes=JOB_INTERVAL,
        id='check_current_exchange_rate',
        replace_existing=True,
    )
    scheduler.start()
    await set_commands(bot)

    try:
        await dp.start_polling()
    finally:
        scheduler.shutdown()
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as e:
        logger.warning(f'Bot stopped! {e}')
