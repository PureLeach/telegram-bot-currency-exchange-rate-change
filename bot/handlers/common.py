from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import BotCommand

from controllers import CurrencyController, UserController


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


async def actions_cancel(message: types.Message, state: FSMContext):
    """Cancellation of actions"""
    await state.finish()
    await message.answer('You canceled the operation', reply_markup=types.ReplyKeyboardRemove())


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands='start')
    dp.register_message_handler(get_help, commands='help')
    dp.register_message_handler(actions_cancel, commands='cancel', state='*')
    dp.register_message_handler(actions_cancel, Text(equals='cancel', ignore_case=True), state='*')


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
        BotCommand(command='/cancel', description='Cancel current action'),
    ]
    await bot.set_my_commands(commands)
