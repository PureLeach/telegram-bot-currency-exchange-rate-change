from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import BotCommand

from controllers import CurrencyController, UserController
from models.exceptions import CurrencyException
from services import exchange_rate
from services.exceptions import CBRException


async def send_welcome(message: types.Message):
    """Greeting the user and adding him to the database"""
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
        '/remove_notification - remove notification\n'
        '/remove_all_notification - remove all notification\n'
        '/cancel - cancel the action\n'
        '/help - reference'
    )


async def send_current_exchange_rate(message: types.Message):
    """Sending the user the current exchange rate of the currencies he subscribed to"""
    try:
        data = await exchange_rate.get_current_exchange_rate_for_user(message.from_user.id)
        await message.reply('Current exchange rates:\n\n' + data)
    except CurrencyException:
        await message.reply("""You don't have currency subscriptions. To subscribe, use the command /subscribe""")
    except CBRException:
        await message.reply('The service is temporarily unavailable')


async def get_list_sub_or_unsub_currencies(message: types.Message, state: FSMContext):
    """Output for the user a list of currencies for which he can subscribe/unsubscribe"""
    action = message.get_command()[1:]
    data = await exchange_rate.get_user_currency_data(message.from_user.id, action)
    if action == 'subscribe':
        await message.reply('List of currencies available for subscribing:\n\n' + data)
        await state.set_data(data={'action': 'subscribe'})
    else:
        await message.reply('List of currencies available for unsubscribing:\n\n' + data)
        await state.set_data(data={'action': 'unsubscribe'})


async def sub_or_unsub_to_currency(message: types.Message, state: FSMContext):
    """Subscription/unsubscription of the user from the selected currency"""
    currency_char_code = message.get_command()[1:]
    action = (await state.get_data()).get('action', 'subscribe')
    if action == 'subscribe':
        await CurrencyController.add_currency_to_user(message.from_user.id, [currency_char_code.lower()])
        await message.reply(f'You have subscribed to the currency {currency_char_code}')
    else:
        await CurrencyController.remove_currency_to_user(message.from_user.id, [currency_char_code.lower()])
        await message.reply(f'You have unsubscribed from the currency {currency_char_code}')


def register_common_handlers(dp: Dispatcher, data: dict):
    # NOTE Добавить логирование в мидлваре
    dp.register_message_handler(send_welcome, commands='start')
    dp.register_message_handler(get_help, commands='help')
    dp.register_message_handler(send_current_exchange_rate, commands='current')
    dp.register_message_handler(get_list_sub_or_unsub_currencies, commands=['subscribe', 'unsubscribe'])
    dp.register_message_handler(sub_or_unsub_to_currency, commands=data['all_currencies'])


async def set_commands(bot: Bot):
    """Registration of commands displayed in the Telegram interface"""
    commands = [
        BotCommand(command='/current', description='Show the current exchange rate'),
        BotCommand(command='/subscribe', description='Subscribe to the exchange rate'),
        BotCommand(command='/unsubscribe', description='Unsubscribe from the exchange rate'),
        BotCommand(command='/list_notification', description='Display a list of notifications'),
        BotCommand(command='/add_notification', description='Add a notification'),
        BotCommand(command='/remove_notification', description='Remove notification'),
        BotCommand(command='/remove_all_notification', description='Remove all notification'),
        BotCommand(command='/help', description='Reference'),
        BotCommand(command='/cancel', description='Отменить текущее действие'),
    ]
    await bot.set_my_commands(commands)
