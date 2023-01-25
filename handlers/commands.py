from aiogram import Dispatcher, types

from models.user import User
from services import api_client


async def send_welcome(message: types.Message):
    # NOTE Добавить логи
    # NOTE Вынести создание пользователя в отдельный метод
    db_session = message.bot.get('db')
    async with db_session() as session:
        await session.merge(
            User(
                id=message.from_user.id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
            )
        )
        await session.commit()
    await message.reply(
        'Hi! This bot is designed to track the exchange rate and notify you when the rate reaches the value you set.\n\n'
        'To get tips on how to use the bot, use the command /help'
    )


async def get_help(message: types.Message):
    await message.reply(
        'Список доступных команд:\n\n'
        '/current - показать текущий курс валют\n'
        '/subscribe - подписаться на курс валют\n'
        '/unsubscribe - отписаться от курса валют\n'
        '/list_notification - вывести список уведомлений\n'
        '/add_notification - добавить уведомление\n'
        '/remove_notification - удалить уведомление\n'
        '/remove_all_notification - удалить все уведомление\n'
        '/help - справка'
    )


async def send_current_exchange_rate(message: types.Message):
    # NOTE Добавить настройку пользователя какие валюты выводить (нужна БД для сохранения настроек пользователей)
    # NOTE Добавить эмодзи
    data = await api_client.get_current_exchange_rate()
    # NOTE добавить pydantic
    usd = data['Valute']['USD']['Value']
    eur = data['Valute']['EUR']['Value']
    await message.reply('Current exchange rates:\n\n' f'USD: {usd}\n' f'EUR: {eur}')


def register_commands(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands='start')
    dp.register_message_handler(get_help, commands='help')
    dp.register_message_handler(send_current_exchange_rate, commands='current')
