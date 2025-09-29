from psycopg import AsyncConnection
from core.tables import Tables
from schemas.notification_schemas import UpdateNotificationRead, UserNotificationColumns, NotificationsStatus, \
    CreateNotifications
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response
from datetime import datetime



async def add_notification_to_user_model(
        connection: AsyncConnection,
        notification: CreateNotifications
):
    with exception_response():

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.NOTIFICATIONS.value)
            .values(notification)
            .execute()
        )

        return builder


async def fetch_all_user_notification_model(
        connection: AsyncConnection,
        user_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.NOTIFICATIONS.value)
            .where(UserNotificationColumns.USER.value, user_id)
            .fetch_all()
        )

        return builder



async def remove_single_user_notification_model(
        connection: AsyncConnection,
        notification_id: str
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.NOTIFICATIONS.value)
            .check_exists({UserNotificationColumns.ID.value: notification_id})
            .where({UserNotificationColumns.ID.value: notification_id})
            .returning(UserNotificationColumns.ID.value)
            .execute()
        )

        return builder



async def remove_all_user_notifications_model(
        connection: AsyncConnection,
        user_id: str
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.NOTIFICATIONS.value)
            .check_exists({UserNotificationColumns.USER.value: user_id})
            .where({UserNotificationColumns.USER.value: user_id})
            .returning(UserNotificationColumns.USER.value)
            .execute()
        )

        return builder



async def update_user_notification_after_read_model(
        connection: AsyncConnection,
        notification_id: str
):
    with exception_response():

        __read_notification__ = UpdateNotificationRead(
            status=NotificationsStatus.OPENED,
            read_at=datetime.now()
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.NOTIFICATIONS.value)
            .values(__read_notification__)
            .check_exists({UserNotificationColumns.ID.value: notification_id})
            .where({UserNotificationColumns.ID.value: notification_id})
            .returning(UserNotificationColumns.ID.value)
            .execute()
        )

        return builder