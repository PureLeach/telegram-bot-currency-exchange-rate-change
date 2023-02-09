import typing as t

from flag import flag

from models.notification import Notification
from services.exchange_rate import get_data_current_exchange_rate


async def get_notifications_data(notifications: t.List[Notification]) -> str:
    """Generating data for displaying a list of user notifications"""
    current_exchange_rate = await get_data_current_exchange_rate()
    data = ''
    for index, notification in enumerate(notifications, start=1):
        user_value = notification.value
        currency_char = notification.currency_char_code
        current_value = getattr(current_exchange_rate.currency, currency_char).value
        data += f'{index}. {flag(currency_char[:2])} {user_value} - current value: {current_value}\n'
    return data
