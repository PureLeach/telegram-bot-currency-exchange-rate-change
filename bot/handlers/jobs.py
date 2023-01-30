from aiogram import Bot
from flag import flag

from controllers import NotificationController
from services.exchange_rate import get_current_exchange_rate


async def check_current_exchange_rate(bot: Bot):
    """
    A periodic task that runs once an hour.
    When the exchange rate reaches the value set by the user,
    bot sends a push notification.
    """
    data = await get_current_exchange_rate()
    notifications_gt, notifications_lt = await NotificationController.get_all_notification()

    for notification in notifications_gt:
        current_value = getattr(data.valute, notification.currency_char_code).value
        if current_value >= notification.value:
            await bot.send_message(
                notification.user_id,
                f'The {flag(notification.currency_char_code[:2])} exchange rate has reached the threshold you set at {notification.value}\n'
                f'Current value: {current_value}',
            )
            await NotificationController.delete(notification)

    for notification in notifications_lt:
        current_value = getattr(data.valute, notification.currency_char_code).value
        if current_value <= notification.value:
            await bot.send_message(
                notification.user_id,
                f'The {flag(notification.currency_char_code[:2])} exchange rate has reached the threshold you set at {notification.value}\n'
                f'Current value: {current_value}',
            )
            await NotificationController.delete(notification)
