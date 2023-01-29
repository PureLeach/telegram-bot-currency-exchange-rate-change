from aiogram import Dispatcher, types

from controllers.user import UserController
from controllers.сurrency import CurrencyController
from models.exceptions import CurrencyException
from services.api_client import ExchangeRateClient
from services.exceptions import CBRException


async def send_welcome(message: types.Message):
    _, created = await UserController.get_or_create(
        id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
    )
    if created:
        await CurrencyController.add_currency_to_user(message.from_user.id, ['usd', 'eur'])
    await message.reply(
        'Hi! This bot is designed to track the exchange rate and notify you when the rate reaches the value you set.\n\n'
        'To get tips on how to use the bot, use the command /help'
    )


async def get_help(message: types.Message):
    await message.reply(
        'List of available commands:\n\n'
        '/current - show the current exchange rate\n'
        '/subscribe - subscribe to the exchange rate\n'
        '/unsubscribe - unsubscribe from the exchange rate\n'
        '/list_notification - display a list of notifications\n'
        '/add_notification - add a notification\n'
        '/remove_notification - delete notification\n'
        '/remove_all_notification - delete all notification\n'
        '/help - reference'
    )


async def send_current_exchange_rate(message: types.Message):
    try:
        data = await ExchangeRateClient.get_current_exchange_rate(message.from_user.id)
        await message.reply('Current exchange rates:\n\n' + data)
    except CurrencyException:
        await message.reply("""You don't have currency subscriptions. To subscribe, use the command /subscribe""")
    except CBRException:
        await message.reply('The service is temporarily unavailable')


async def get_list_sub_currencies(message: types.Message):
    # NOTE Выводить только те валюты на которые пользователь ещё не подписан
    await message.reply(
        'List of currencies available for subscribing:\n\n'
        '/USD - Dollar США\n'
        '/EUR - Euro\n'
        '/EGP - Egyptian pounds'
    )


async def subscribe_currency(message: types.Message):
    """User's subscription to currencies"""
    currency_char_code = message.get_command()[1:]
    await CurrencyController.add_currency_to_user(message.from_user.id, [currency_char_code.lower()])
    await message.reply(f'You have subscribed to the currency {currency_char_code}')


async def unsubscribe_currency(message: types.Message):
    """Unsubscribing a user from a currency"""
    # NOTE Машина состояний чтобы знать какая прошлая команда была задана
    currency_char_code = message.get_command()[1:]
    await CurrencyController.remove_currency_to_user(message.from_user.id, [currency_char_code.lower()])
    await message.reply(f'You have unsubscribed from the currency {currency_char_code}')


def register_commands(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands='start')
    dp.register_message_handler(get_help, commands='help')
    dp.register_message_handler(send_current_exchange_rate, commands='current')
    dp.register_message_handler(get_list_sub_currencies, commands='subscribe')
    dp.register_message_handler(get_list_sub_currencies, commands='unsubscribe')
    dp.register_message_handler(subscribe_currency, commands=['USD', 'EUR', 'EGP'])
