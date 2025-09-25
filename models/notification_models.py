from psycopg import AsyncConnection

from schemas.notification_schemas import UpdateNotificationRead
from utils import exception_response


async def fetch_all_user_notification_model(
        connection: AsyncConnection,
        user_id: str
):
    with exception_response():
        pass


async def remove_single_user_notification_model(
        connection: AsyncConnection,
        notification_id: str
):
    with exception_response():
        pass


async def remove_all_user_notifications_model(
        connection: AsyncConnection,
        user_id: str
):
    with exception_response():
        pass


async def update_user_notification_after_read_model(
        connection: AsyncConnection,
        notification: UpdateNotificationRead,
        notification_id: str
):
    with exception_response():
        pass