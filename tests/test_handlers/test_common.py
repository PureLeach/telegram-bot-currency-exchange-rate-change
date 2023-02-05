from unittest.mock import AsyncMock, patch

import pytest

from bot.handlers.common import send_welcome


@pytest.mark.asyncio
async def test_start_handlers():
    message = AsyncMock()
    with patch('controllers.user.UserController.get_or_create', return_value=('user', False)):
        await send_welcome(message)
    message.reply.assert_called_once_with(
        'Hi! This bot is designed to track the exchange rate and notify you when the rate reaches the value you set.\n\n'
        'To get tips on how to use the bot, use the command /help'
    )
