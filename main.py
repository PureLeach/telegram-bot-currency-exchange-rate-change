from aiogram import Bot, Dispatcher, executor, types
from environs import Env

env = Env()
env.read_env(override=True)

API_TOKEN = env.str('API_TOKEN')

bot = Bot(token=API_TOKEN)


dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        'Привет! Этот бот предназначен для отслеживания курса валют и уведомления, когда курс достигнет заданного вами значения.\
\n\nЧтобы получить подсказку, как пользоваться ботом, воспользуйся командой /help'
    )


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp)
