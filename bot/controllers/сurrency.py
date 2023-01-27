from sqlalchemy import select
from sqlalchemy.exc import InvalidRequestError

from db.base import async_session
from models import Currency, User
from settings import logger


class CurrencyController:
    @staticmethod
    async def get_currency(currency_char_code: str) -> Currency:
        async with async_session() as session:
            statement = await session.execute(select(Currency).where(Currency.char_code == currency_char_code))
            сurrency: Currency = statement.scalar()
            return сurrency

    @staticmethod
    async def add_currency_to_user(user_id: int, currency_char_code: str) -> None:
        сurrency = await CurrencyController.get_currency(currency_char_code)
        try:
            async with async_session() as session:
                user: User = await session.get(User, user_id)
                user.currencies = [сurrency]
                await session.commit()
        except InvalidRequestError as e:
            logger.error(
                f'Ошибка при добавлении валюты к пользователю: user_id={user_id}, сurrency={currency_char_code}, error={e}'
            )
