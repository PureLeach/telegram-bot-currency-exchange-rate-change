from aiogram import Bot


async def send_message_cron(bot: Bot):
    await bot.send_message(123, 'Это сообщение будет отправляться ежедневно в указанное время.')
