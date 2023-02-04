import typing as t

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError

from models import Notification
from settings.core import logger
from settings.db import async_session


class NotificationController:
    @staticmethod
    async def create(**kwargs) -> Notification:
        try:
            async with async_session() as session:
                notification = Notification(**kwargs)
                session.add(notification)
                await session.commit()
                return notification
        except SQLAlchemyError as e:
            logger.warning(f'Error when creating notification: error={e}')

    @staticmethod
    async def delete(notification: Notification) -> Notification:
        try:
            async with async_session() as session:
                await session.delete(notification)
                await session.commit()
        except SQLAlchemyError as e:
            logger.warning(f'Error when deleting notification: error={e}')

    @staticmethod
    async def get_all_notifications() -> t.Tuple[t.List[Notification], t.List[Notification]]:
        try:
            async with async_session() as session:
                result = await session.execute(select(Notification).filter(Notification.comparison_sign == '>'))
                notifications_gt: t.List[Notification] = result.unique().scalars().all()
                result = await session.execute(select(Notification).filter(Notification.comparison_sign == '<'))
                notifications_lt: t.List[Notification] = result.unique().scalars().all()
                return notifications_gt, notifications_lt
        except SQLAlchemyError as e:
            logger.warning(f'Error when getting all notifications: error={e}')

    @staticmethod
    async def get_all_user_notifications(user_id: int) -> t.List[Notification]:
        try:
            async with async_session() as session:
                result = await session.execute(select(Notification).filter(Notification.user_id == user_id))
                notifications: t.List[Notification] = result.unique().scalars().all()
                return notifications
        except SQLAlchemyError as e:
            logger.warning(f'Error when getting all user notifications: user_id={user_id}, error={e}')

    @staticmethod
    async def delete_all_user_notifications(user_id: int) -> None:
        try:
            async with async_session() as session:
                await session.execute(delete(Notification).filter(Notification.user_id == user_id))
                await session.commit()
        except SQLAlchemyError as e:
            logger.warning(f'Error when deleting all user notifications: user_id={user_id}, error={e}')
