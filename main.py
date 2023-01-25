from aiogram import Bot, Dispatcher, executor, types

import client
from settings import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        'Hi! This bot is designed to track the exchange rate and notify you when the rate reaches the value you set.\n\n'
        'To get tips on how to use the bot, use the command /help'
    )


@dp.message_handler(commands=['help'])
async def get_help(message: types.Message):
    await message.reply(
        'Список доступных команд:\n\n'
        '/current - показать текущий курс валют\n'
        '/subscribe - подписаться на курс валют\n'
        '/unsubscribe - отписаться от курса валют\n'
        '/list_notification - вывести список уведомлений\n'
        '/add_notification - добавить уведомление\n'
        '/remove_notification - удалить уведомление\n'
        '/remove_all_notification - удалить все уведомление\n'
        '/help - справка'
    )


@dp.message_handler(commands=['current'])
async def send_current_exchange_rate(message: types.Message):
    # NOTE Добавить настройку пользователя какие валюты выводить (нужна БД для сохранения настроек пользователей)
    # NOTE Добавить эмодзи
    data = await client.get_current_exchange_rate()
    # NOTE добавить pydantic
    usd = data['Valute']['USD']['Value']
    eur = data['Valute']['EUR']['Value']
    await message.reply('Current exchange rates:\n\n' f'USD: {usd}\n' f'EUR: {eur}')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
