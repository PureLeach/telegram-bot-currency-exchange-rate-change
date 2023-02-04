import typing as t

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models import Currency, User
from settings.core import logger
from settings.db import async_session


class CurrencyController:
    @staticmethod
    async def get_all_currencies() -> t.List[Currency]:
        try:
            async with async_session() as session:
                result = await session.execute(select(Currency))
                currencies: t.List[Currency] = result.unique().scalars().all()
                return currencies
        except SQLAlchemyError as e:
            logger.error(f'Error when getting all currencies: error={e}')

    @staticmethod
    async def get_currencies_by_codes(currency_char_codes: list) -> t.List[Currency]:
        try:
            async with async_session() as session:
                result = await session.execute(select(Currency).filter(Currency.char_code.in_(currency_char_codes)))
                currencies: Currency = result.unique().scalars().all()
                return currencies
        except SQLAlchemyError as e:
            logger.error(f'Error when getting currency by codes: currency_char_codes={currency_char_codes}, error={e}')

    @staticmethod
    async def add_currency_to_user(user_id: int, currency_char_codes: list) -> None:
        currencies = await CurrencyController.get_currencies_by_codes(currency_char_codes)
        try:
            async with async_session() as session:
                user: User = await session.get(User, user_id)
                user.currencies.extend(currencies)
                await session.commit()
        except SQLAlchemyError as e:
            logger.error(
                f'Error when adding currency to a user: user_id={user_id}, currency={currency_char_codes}, error={e}'
            )

    @staticmethod
    async def remove_currency_to_user(user_id: int, currency_char_codes: list) -> None:
        try:
            async with async_session() as session:
                user: User = await session.get(User, user_id)
                user.currencies = [
                    currency for currency in user.currencies if currency.char_code not in currency_char_codes
                ]
                await session.commit()
        except SQLAlchemyError as e:
            logger.error(
                f'Error when remove currency to a user: user_id={user_id}, currency={currency_char_codes}, error={e}'
            )
