from aiogram import Bot
from aiogram.utils.exceptions import ChatNotFound
from flag import flag

from controllers import NotificationController
from services.exchange_rate import get_current_exchange_rate


async def check_current_exchange_rate(bot: Bot):
    """
    A periodic task that runs once an hour.
    When the exchange rate reaches the value set by the user,
    bot sends a push notification.
    """
    # NOTE Логи
    current_exchange_rate = await get_current_exchange_rate(actual=True)
    notifications_gt, notifications_lt = await NotificationController.get_all_notifications()
    users = []
    for notification in notifications_gt:
        current_value = getattr(current_exchange_rate.valute, notification.currency_char_code).value
        if current_value >= notification.value:
            users.append(
                {
                    'user_id': notification.user_id,
                    'flag': flag(notification.currency_char_code[:2]),
                    'users_value': notification.value,
                    'current_value': current_value,
                    'notification': notification,
                }
            )

    for notification in notifications_lt:
        current_value = getattr(current_exchange_rate.valute, notification.currency_char_code).value
        if current_value <= notification.value:
            users.append(
                {
                    'user_id': notification.user_id,
                    'flag': flag(notification.currency_char_code[:2]),
                    'users_value': notification.value,
                    'current_value': current_value,
                    'notification': notification,
                }
            )

    for user_data in users:
        try:
            await bot.send_message(
                user_data.get('user_id'),
                f"""The {user_data.get('flag')} exchange rate has reached the threshold you set at {user_data.get('users_value')}\n"""
                f"""Current value: {user_data.get('current_value')}""",
            )
        except ChatNotFound as e:
            # NOTE Лог Чат не был найден, уведомление для него будет удалено.
            print(f'\033[31m e, { e }, {type(e)} \033[0m')
        await NotificationController.delete(user_data['notification'])
