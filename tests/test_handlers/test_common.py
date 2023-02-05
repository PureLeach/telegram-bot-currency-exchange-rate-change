from unittest.mock import AsyncMock, patch

import pytest
from aiogram import types

from bot.handlers import common


@pytest.mark.asyncio
async def test_send_welcome():
    message = AsyncMock()
    with patch('controllers.user.UserController.get_or_create', return_value=('user', False)):
        await common.send_welcome(message)

    message.reply.assert_called_once_with(
        'Hi! This bot is designed to track the exchange rate and notify you when the rate reaches the value you set.\n\n'
        'To get tips on how to use the bot, use the command /help'
    )


@pytest.mark.asyncio
async def test_get_help():
    message = AsyncMock()
    await common.get_help(message)

    message.reply.assert_called_once_with(
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


@pytest.mark.asyncio
async def test_actions_cancel():
    message = AsyncMock()
    state = AsyncMock()
    await common.actions_cancel(message, state)

    message.answer.assert_called_once_with('You canceled the operation', reply_markup=types.ReplyKeyboardRemove())
