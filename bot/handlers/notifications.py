from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from pydantic import ValidationError

from controllers.notification import NotificationController
from schemas.exchange_rate import CurrencyValue
from services.exchange_rate import get_current_exchange_value
from services.notifications import get_notifications_data
from services.utils import get_dict_flag_currencies, get_list_flag_currencies
from states.notification import AddNotificationState, RemoveAllNotificationState, RemoveNotificationState


async def actions_cancel(message: types.Message, state: FSMContext):
    """Canceling the notification addition process"""
    await state.finish()
    await message.answer('You canceled the operation', reply_markup=types.ReplyKeyboardRemove())


async def add_notification(message: types.Message, state: FSMContext):
    """Starting the process of adding a new notification"""
    # NOTE Добавить логи
    flag_currencies_list = await get_list_flag_currencies()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*flag_currencies_list)
    await message.answer('Select the currency for which you want to set the notification', reply_markup=keyboard)
    await state.set_state(AddNotificationState.waiting_for_currency_selection.state)


async def currency_chosen(message: types.Message, state: FSMContext):
    """User's choice of the currency at which the notification will be received"""
    emoji_currency = message.text.lower()
    flag_currencies_dict = await get_dict_flag_currencies()
    if emoji_currency not in flag_currencies_dict.keys():
        await message.answer('Please select the currency using the keyboard below')
        return
    await state.update_data(
        chosen_currency_char=flag_currencies_dict.get(emoji_currency), chosen_currency_flag=emoji_currency
    )
    await state.set_state(AddNotificationState.waiting_for_value_input.state)
    await message.answer('Enter the value at which you need to be notified', reply_markup=types.ReplyKeyboardRemove())


async def value_chosen(message: types.Message, state: FSMContext):
    """Setting by the user the currency value at which the notification will be received"""
    try:
        user_value = CurrencyValue(value=message.text).value
    except ValidationError:
        await message.answer('Please enter the correct value of the number')
        return
    user_data = await state.get_data()
    currency_char = user_data.get('chosen_currency_char')
    current_value = await get_current_exchange_value(currency_char)
    if current_value == user_value:
        await message.answer('The value you specified has already been reached at the moment')
        await state.finish()
        return
    comparison_sign = '<' if current_value > user_value else '>'
    await NotificationController.create(
        user_id=message.from_user.id,
        currency_char_code=currency_char,
        value=user_value,
        comparison_sign=comparison_sign,
    )
    await message.answer(
        f"""A notification for the value of {user_value} {user_data.get('chosen_currency_flag')} currency has been added.\n\n"""
        'You will receive a notification when the specified currency reaches this value'
    )
    await state.finish()


async def list_notification(message: types.Message):
    """Output of all notifications"""
    notifications = await NotificationController.get_all_user_notifications(message.from_user.id)
    if not notifications:
        await message.reply("""You have not yet had any notifications created""")
        return
    data = await get_notifications_data(notifications)
    await message.reply('List your notifications:\n\n' + data)


async def remove_notification(message: types.Message, state: FSMContext):
    """Deleting the user's notifications"""
    notifications = await NotificationController.get_all_user_notifications(message.from_user.id)
    data = await get_notifications_data(notifications)
    index_with_notification = {str(index): notification for index, notification in enumerate(notifications, start=1)}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*index_with_notification.keys())
    await message.answer('List your notifications:\n\n' + data)
    await message.answer('Enter the notification number to delete it', reply_markup=keyboard)
    await state.update_data(index_with_notification=index_with_notification)
    await state.set_state(RemoveNotificationState.waiting_for_index_input.state)


async def index_chosen(message: types.Message, state: FSMContext):
    """User's choice of the notification number that he wants to delete"""
    user_data = await state.get_data()
    index_with_notification = user_data.get('index_with_notification')
    if message.text not in index_with_notification.keys():
        await message.answer('Please select the index using the keyboard below')
        return
    await NotificationController.delete(index_with_notification.get(message.text))
    await message.answer('The notification has been deleted', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def remove_all_notification(message: types.Message, state: FSMContext):
    """Deleting all notifications for the user"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('YES', 'NO')
    await message.answer('Do you really want to delete all your notifications?', reply_markup=keyboard)
    await state.set_state(RemoveAllNotificationState.waiting_for_response.state)


async def confirmation_chosen(message: types.Message, state: FSMContext):
    """User's choice of the notification number that he wants to delete"""
    if message.text.lower() not in ('yes', 'no'):
        await message.answer('Please make your selection using the keypad')
        return
    if message.text.lower() == 'yes':
        await NotificationController.delete_all_user_notifications(message.from_user.id)
        await message.answer('The notifications has been deleted', reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer('Deletion canceled', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_notification_handlers(dp: Dispatcher):
    dp.register_message_handler(actions_cancel, commands='cancel', state='*')
    dp.register_message_handler(actions_cancel, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(add_notification, commands='add_notification', state='*')
    dp.register_message_handler(currency_chosen, state=AddNotificationState.waiting_for_currency_selection)
    dp.register_message_handler(value_chosen, state=AddNotificationState.waiting_for_value_input)
    dp.register_message_handler(list_notification, commands='list_notification')
    dp.register_message_handler(remove_notification, commands='remove_notification', state='*')
    dp.register_message_handler(index_chosen, state=RemoveNotificationState.waiting_for_index_input)
    dp.register_message_handler(remove_all_notification, commands='remove_all_notification', state='*')
    dp.register_message_handler(confirmation_chosen, state=RemoveAllNotificationState.waiting_for_response)
