from psycopg import AsyncConnection

from core.tables import Tables
from schemas.engagement_staff_schemas import NewEngagementStaff, UpdateStaff, CreateEngagementStaff, \
    EngagementStaffColumns
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key


async def create_new_engagement_staff_model(
        connection: AsyncConnection,
        staff: NewEngagementStaff,
        engagement_id: str,
):
    with exception_response():
        __staff__ = CreateEngagementStaff(
            id=get_unique_key(),
            engagement=engagement_id,
            name=staff.name,
            email=staff.email,
            role=staff.role,
            start_date=staff.start_date,
            end_date=staff.end_date,
            tasks=staff.tasks
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENT_STAFF.value)
            .values(__staff__)
            .check_exists({EngagementStaffColumns.NAME.value: staff.name})
            .check_exists({EngagementStaffColumns.ROLE.value: staff.role})
            .returning(EngagementStaffColumns.ID.value)
            .execute()
        )

        return builder


async def fetch_engagement_staff_model(
        connection: AsyncConnection,
        engagement_id: str,
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ENGAGEMENT_STAFF.value)
            .where(EngagementStaffColumns.ENGAGEMENT.value, engagement_id)
            .fetch_all()
        )

        return builder


async def update_staff_model(
        connection: AsyncConnection,
        staff: UpdateStaff,
        staff_id: str,
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENT_STAFF.value)
            .values(staff)
            .check_exists({EngagementStaffColumns.ID.value: staff_id})
            .where({EngagementStaffColumns.ID.value: staff_id})
            .returning(EngagementStaffColumns.ID.value)
            .execute()
        )

        return builder


async def delete_staff_model(
        connection: AsyncConnection,
        staff_id: str,
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.ENGAGEMENT_STAFF.value)
            .check_exists({EngagementStaffColumns.ID.value: staff_id})
            .where({EngagementStaffColumns.ID.value: staff_id})
            .returning(EngagementStaffColumns.ID.value)
            .execute()
        )

        return builder