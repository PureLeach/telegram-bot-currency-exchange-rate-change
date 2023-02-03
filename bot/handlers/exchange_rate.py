from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from controllers import CurrencyController
from models.exceptions import CurrencyException
from services.currencies import get_user_currency_data
from services.exceptions import CBRException
from services.exchange_rate import get_current_exchange_rate_for_user


async def send_current_exchange_rate(message: types.Message):
    """Sending the user the current exchange rate of the currencies he subscribed to"""
    try:
        data = await get_current_exchange_rate_for_user(message.from_user.id)
        await message.reply('Current exchange rates:\n\n' + data)
    except CurrencyException:
        await message.reply("""You don't have currency subscriptions. To subscribe, use the command /subscribe""")
    except CBRException:
        await message.reply('The service is temporarily unavailable')


async def get_list_sub_or_unsub_currencies(message: types.Message, state: FSMContext):
    """Output for the user a list of currencies for which he can subscribe/unsubscribe"""
    action = message.get_command()[1:]
    data = await get_user_currency_data(message.from_user.id, action)
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


def register_exchange_rate_handlers(dp: Dispatcher, data: dict):
    # NOTE Добавить логирование в мидлваре
    dp.register_message_handler(send_current_exchange_rate, commands='current')
    dp.register_message_handler(get_list_sub_or_unsub_currencies, commands=['subscribe', 'unsubscribe'])
    dp.register_message_handler(sub_or_unsub_to_currency, commands=data['all_currencies'])
