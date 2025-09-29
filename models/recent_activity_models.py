from psycopg import AsyncConnection
from core.tables import Tables
from schemas.recent_activities_schemas import RecentActivities, RecentActivityColumns
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from utils import exception_response


async def add_new_recent_activity(
        connection: AsyncConnection,
        recent_activity: RecentActivities,
):
    with exception_response():
        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.RECENT_ACTIVITIES.value)
            .values(recent_activity)
            .returning(RecentActivityColumns.ACTIVITY_ID.value)
            .execute()
        )

        return builder



async def fetch_recent_activities(
        connection: AsyncConnection,
        module_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.RECENT_ACTIVITIES.value)
            .where(RecentActivityColumns.MODULE_ID.value, module_id)
            .limit(20)
            .fetch_all()
        )

        return builder