from aiogram import Dispatcher, types

from controllers.user import UserController
from controllers.сurrency import CurrencyController
from services.api_client import ExchangeRateClient


async def send_welcome(message: types.Message):
    await UserController.create(
        id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
    )
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
    data = await ExchangeRateClient.get_current_exchange_rate(message.from_user.id)
    await message.reply('Current exchange rates:\n\n' + data)


async def get_list_currencies(message: types.Message):
    await message.reply('Список доступных валют:\n\n' '/USD - Доллар США\n' '/EUR - Евро\n' '/EGP - Египетских фунтов')


async def subscribe_currency(message: types.Message):
    """Подписка пользователя на валюты"""
    currency_char_code = message.get_command()[1:]
    await CurrencyController.add_currency_to_user(message.from_user.id, currency_char_code.lower())
    await message.reply(f'Вы подписались на валюту {currency_char_code}')


def register_commands(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands='start')
    dp.register_message_handler(get_help, commands='help')
    dp.register_message_handler(send_current_exchange_rate, commands='current')
    dp.register_message_handler(get_list_currencies, commands='subscribe')
    dp.register_message_handler(subscribe_currency, commands=['USD', 'EUR', 'EGP'])
