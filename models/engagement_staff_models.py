from datetime import datetime
from psycopg import AsyncConnection
from core.tables import Tables
from schemas.engagement_staff_schemas import NewEngagementStaff, UpdateStaff, CreateEngagementStaff, \
    EngagementStaffColumns, ReadEngagementStaff, Stage, ActualStaffTimesheet
from schemas.role_schemas import BaseRole
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
            user_id=staff.user_id,
            role_id=staff.role_id,
            role=staff.role,
            name=staff.name,
            email=staff.email,
            planning=Stage(
                hours=staff.planning.hours,
                start_date=staff.planning.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                end_date=staff.planning.end_date.strftime("%Y-%m-%d %H:%M:%S"),
            ),
            fieldwork=Stage(
                hours=staff.planning.hours,
                start_date=staff.fieldwork.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                end_date=staff.fieldwork.end_date.strftime("%Y-%m-%d %H:%M:%S"),
            ),
            reporting=Stage(
                hours=staff.reporting.hours,
                start_date=staff.reporting.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                end_date=staff.reporting.end_date.strftime("%Y-%m-%d %H:%M:%S"),
            ),
            finalization=Stage(
                hours=staff.reporting.hours,
                start_date=staff.finalization.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                end_date=staff.finalization.end_date.strftime("%Y-%m-%d %H:%M:%S"),
            ),
            id=get_unique_key(),
            engagement=engagement_id,
            created_at=datetime.now(),
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENT_STAFF.value)
            .values(__staff__)
            .check_exists({EngagementStaffColumns.USER_ID.value: staff.user_id})
            .check_exists({EngagementStaffColumns.ROLE_ID.value: staff.role_id})
            .check_exists({EngagementStaffColumns.ENGAGEMENT.value: engagement_id})
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


async def fetch_engagement_staff_data_model(
        connection: AsyncConnection,
        engagement_id: str,
        user_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ENGAGEMENT_STAFF.value, alias="eng_staff")
            .select(ReadEngagementStaff)
            .join_aggregate(
                join_type="LEFT",
                table=Tables.ROLES.value,
                on="roles.id = eng_staff.role_id",
                alias="roles",
                aggregate_column="id",
                json_field_name="role",
                model=BaseRole,
                use_prefix=True,
                as_object=True
            )
            .where(EngagementStaffColumns.ENGAGEMENT.value, engagement_id)
            .where(EngagementStaffColumns.USER_ID.value, user_id)
            .select_joins()
            .fetch_one()
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


async def update_user_timesheet_model(
        connection: AsyncConnection,
        staff: ActualStaffTimesheet,
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

