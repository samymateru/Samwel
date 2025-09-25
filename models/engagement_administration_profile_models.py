from psycopg import AsyncConnection

from core.tables import Tables
from schemas.engagement_administration_profile_schemas import NewEngagementAdministrationProfile, \
    EngagementProfileColumns
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response


async def update_engagement_profile_model(
        connection: AsyncConnection,
        profile: NewEngagementAdministrationProfile,
        engagement_id: str
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENT_PROFILE.value)
            .values(profile)
            .check_exists({EngagementProfileColumns.ID.value: engagement_id})
            .where({EngagementProfileColumns.ID.value: engagement_id})
            .returning(EngagementProfileColumns.ID.value)
            .execute()
        )
        return builder


async def fetch_engagement_administration_profile_model(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ENGAGEMENT_PROFILE.value)
            .where(EngagementProfileColumns.ENGAGEMENT.value, engagement_id)
            .fetch_one()
        )

        return builder