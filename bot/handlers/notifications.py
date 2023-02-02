from decimal import Decimal, InvalidOperation

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from controllers.notification import NotificationController
from services.exchange_rate import get_current_exchange_rate
from services.utils import get_dict_flag_currencies, get_list_flag_currencies
from states.notification import AddNotificationState


async def notification_cancel(message: types.Message, state: FSMContext):
    """Canceling the notification addition process"""
    current_state = await state.get_state()
    if current_state in (
        'AddNotificationState:waiting_for_currency_selection',
        'AddNotificationState:waiting_for_value_input',
    ):
        await state.finish()
        await message.answer('Adding a notification has been canceled', reply_markup=types.ReplyKeyboardRemove())


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
    flag_currencies_list = await get_list_flag_currencies()
    emoji_currency = message.text.lower()
    if emoji_currency not in flag_currencies_list:
        await message.answer('Please select the currency using the keyboard below')
        return
    flag_currencies_dict = await get_dict_flag_currencies()
    currency_char = flag_currencies_dict[emoji_currency]
    await state.update_data(chosen_currency_char=currency_char, chosen_currency_flag=emoji_currency)
    await state.set_state(AddNotificationState.waiting_for_value_input.state)
    await message.answer('Enter the value at which you need to be notified', reply_markup=types.ReplyKeyboardRemove())


async def value_chosen(message: types.Message, state: FSMContext):
    """Setting by the user the currency value at which the notification will be received"""
    # NOTE Добавить клавиатуру с числами (точка запятая)
    try:
        user_value = Decimal(message.text).quantize(Decimal('1.0000'))
        if user_value <= 0:
            await message.answer('Please enter the correct value of the number')
            return
        user_data = await state.get_data()
        current_exchange_rate = await get_current_exchange_rate()
        currency_char = user_data.get('chosen_currency_char')
        current_value = getattr(current_exchange_rate.valute, currency_char).value
        if current_value == user_value:
            await message.answer('The value you specified has already been reached at the moment')
            await state.finish()
        else:
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
    except (ValueError, InvalidOperation):
        await message.answer('Please enter the correct value of the number')
        return


async def list_notification(message: types.Message):
    """Output of all notifications"""
    notifications_gt, notifications_lt = await NotificationController.get_all_notification()
    await message.reply(
        'List your notifications:\n\n'
        '1. USD 32.12 - current value: 312.21\n'
        '2. EUR 312.12 - current value: 353.21\n'
    )


async def remove_notification(message: types.Message):
    await message.reply('List of available commands:\n\n')
    # Вывести список добавленных уведомлений с порядковым числом и вызовом клавиатуры

    # При нажатии на соответствующий номер удаляется запись в БД


async def remove_all_notification(message: types.Message):
    await message.reply('List of available commands:\n\n')
    # Вывести клавиатуру с подтверждением удаления всех уведомлений (да/нет)

    # При нажатии на да - удалить все записи уведомлений пользователя

    # При нажатии на нет - сбросить состояние и ничего не делать


def register_handlers_notification(dp: Dispatcher):
    dp.register_message_handler(notification_cancel, commands='cancel', state='*')
    dp.register_message_handler(notification_cancel, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(add_notification, commands='add_notification', state='*')
    dp.register_message_handler(currency_chosen, state=AddNotificationState.waiting_for_currency_selection)
    dp.register_message_handler(value_chosen, state=AddNotificationState.waiting_for_value_input)
    dp.register_message_handler(list_notification, commands='list_notification')
    # dp.register_message_handler(remove_notification, commands='remove_notification')
    # dp.register_message_handler(remove_all_notification, commands='remove_all_notification')
