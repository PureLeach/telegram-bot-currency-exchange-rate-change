import typing as t

from sqlalchemy import delete, select

from models import Notification
from settings.db import async_session


class NotificationController:
    @staticmethod
    async def create(**kwargs) -> Notification:
        async with async_session() as session:
            notification = Notification(**kwargs)
            session.add(notification)
            await session.commit()
            return notification

    @staticmethod
    async def delete(notification: Notification) -> Notification:
        async with async_session() as session:
            await session.delete(notification)
            await session.commit()

    @staticmethod
    async def get_all_notifications() -> t.Tuple[t.List[Notification], t.List[Notification]]:
        async with async_session() as session:
            result = await session.execute(select(Notification).filter(Notification.comparison_sign == '>'))
            notifications_gt: t.List[Notification] = result.unique().scalars().all()
            result = await session.execute(select(Notification).filter(Notification.comparison_sign == '<'))
            notifications_lt: t.List[Notification] = result.unique().scalars().all()
            return notifications_gt, notifications_lt

    @staticmethod
    async def get_all_user_notifications(user_id: int) -> t.List[Notification]:
        async with async_session() as session:
            result = await session.execute(select(Notification).filter(Notification.user_id == user_id))
            notifications: t.List[Notification] = result.unique().scalars().all()
            return notifications

    @staticmethod
    async def delete_all_user_notifications(user_id: int) -> t.List[Notification]:
        async with async_session() as session:
            await session.execute(delete(Notification).filter(Notification.user_id == user_id))
            await session.commit()