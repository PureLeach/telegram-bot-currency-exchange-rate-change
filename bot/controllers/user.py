import typing as t

from sqlalchemy import select

from db.base import async_session
from models import User


class UserController:
    @staticmethod
    async def create(
        id: int, first_name: t.Optional[str], last_name: t.Optional[str], username: t.Optional[str]
    ) -> User:
        async with async_session() as session:
            user: User = await session.merge(
                User(
                    id=id,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                )
            )
            await session.commit()
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
                session.add(User(**kwargs))
                await session.commit()
                return user, True

    @staticmethod
    async def get_users_currencies(id: int) -> list[str]:
        async with async_session() as session:
            user: User = await session.get(User, id)
            currencies = [currency.char_code for currency in user.currencies]
            return currencies
