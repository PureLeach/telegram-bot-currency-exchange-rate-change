import typing as t

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models import User
from settings.core import logger
from settings.db import async_session


class UserController:
    @staticmethod
    async def create(**kwargs) -> User:
        try:
            async with async_session() as session:
                user = User(**kwargs)
                session.add(user)
                await session.commit()
                return user
        except SQLAlchemyError as e:
            logger.warning(f'Error when creating user: error={e}')

    @staticmethod
    async def get(**kwargs) -> User:
        try:
            async with async_session() as session:
                statement = await session.execute(select(User).filter_by(**kwargs))
                user: User = statement.scalar()
                return user
        except SQLAlchemyError as e:
            logger.warning(f'Error when getting user: error={e}')

    @staticmethod
    async def get_or_create(defaults=None, **kwargs) -> t.Tuple[User, bool]:
        try:
            async with async_session() as session:
                statement = await session.execute(select(User).filter_by(**kwargs))
                user: User = statement.scalar()
                if user:
                    return user, False
                else:
                    kwargs |= defaults or {}
                    user = User(**kwargs)
                    session.add(user)
                    await session.commit()
                    return user, True
        except SQLAlchemyError as e:
            logger.warning(f'Error when getting or creating user: error={e}')

    @staticmethod
    async def get_users_currencies(user_id: int) -> t.List[str]:
        try:
            async with async_session() as session:
                user: User = await session.get(User, user_id)
                currencies = [currency.char_code for currency in user.currencies]
                return currencies
        except SQLAlchemyError as e:
            logger.warning(f'Error when getting users currencies: user_id={user_id}, error={e}')
