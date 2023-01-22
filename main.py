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


@dp.message_handler(commands=['current'])
async def send_current_exchange_rate(message: types.Message):
    # NOTE Добавить настройку пользователя какие валюты выводить
    # NOTE Добавить эмодзи
    data = await client.get_current_exchange_rate()
    usd = data['Valute']['USD']['Value']
    eur = data['Valute']['EUR']['Value']
    await message.reply('Current exchange rates:\n\n' f'USD: {usd}\n' f'EUR: {eur}')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
