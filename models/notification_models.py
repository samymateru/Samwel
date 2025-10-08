from typing import List

from psycopg import AsyncConnection
from core.tables import Tables
from models.engagement_staff_models import fetch_engagement_staff_model
from models.issue_actor_models import get_all_issue_actors_on_issue_model
from models.management_models import fetch_organization_management_model
from schemas.issue_actor_schemas import IssueActors, IssueActorColumns
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



async def get_organization_managers_model(
        connection: AsyncConnection,
        organization_id: str,
):
    with exception_response():
        data = await fetch_organization_management_model(
            connection=connection,
            organization_id=organization_id
        )

        return data




async def get_engagements_business_contacts_model(
        connection: AsyncConnection,
        engagement_id: str,
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.BUSINESS_CONTACT)
            .where("engagement", engagement_id)
            .fetch_all()
        )

        return builder



async def get_engagements_audit_contacts_model(
        connection: AsyncConnection,
        engagement_id: str,
):
    with exception_response():
        data = await fetch_engagement_staff_model(
            connection=connection,
            engagement_id=engagement_id
        )

        return data



async def get_issue_contacts_model(
        connection: AsyncConnection,
        issue_id: str,
):
    with exception_response():
        data = await get_all_issue_actors_on_issue_model(
            connection=connection,
            issue_id=issue_id
        )

        return data



async def get_issue_contacts_by_role_model(
        connection: AsyncConnection,
        issue_id: str,
        roles: List[IssueActors]
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ISSUE_ACTORS.value)
            .where(IssueActorColumns.ISSUE_ID.value, issue_id)
            .where(IssueActorColumns.ROLE.value, roles)
            .fetch_all()
        )

        return builder
