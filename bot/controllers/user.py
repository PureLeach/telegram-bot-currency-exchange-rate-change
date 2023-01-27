import typing as t

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
    async def get_users_currencies(id: int) -> list[str]:
        async with async_session() as session:
            user: User = await session.get(User, id)
            currencies = [currency.char_code for currency in user.currencies]
            return currencies
