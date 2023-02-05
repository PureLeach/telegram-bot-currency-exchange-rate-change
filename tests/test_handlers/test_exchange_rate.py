from unittest.mock import AsyncMock, patch

import pytest

from bot.handlers import exchange_rate


@pytest.mark.asyncio
@patch('controllers.user.UserController.get_users_currencies')
@patch('services.exchange_rate.get_data_current_exchange_rate')
@patch('services.exchange_rate.get_data_current_exchange_rate_for_user')
async def test_send_current_exchange_rate(*args, **kwargs):
    message = AsyncMock()
    with patch('services.exchange_rate.collect_users_exchange_rates', return_value='data') as mock:
        await exchange_rate.send_current_exchange_rate(message)
    
    message.reply.assert_called_once_with('Current exchange rates:\n\n' + mock.return_value)

