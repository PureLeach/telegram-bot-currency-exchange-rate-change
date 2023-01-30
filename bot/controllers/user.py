import typing as t

from sqlalchemy import select

from models import User
from settings.db import async_session


class UserController:
    @staticmethod
    async def create(**kwargs) -> User:
        async with async_session() as session:
            user = User(**kwargs)
            session.add(user)
            await session.commit()
            return user

    @staticmethod
    async def get(**kwargs) -> User:
        async with async_session() as session:
            statement = await session.execute(select(User).filter_by(**kwargs))
            user: User = statement.scalar()
            return user

    @staticmethod
    async def get_or_create(defaults=None, **kwargs) -> t.Tuple[User, bool]:
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

    @staticmethod
    async def get_users_currencies(id: int) -> list[str]:
        async with async_session() as session:
            user: User = await session.get(User, id)
            currencies = [currency.char_code for currency in user.currencies]
            return currencies
