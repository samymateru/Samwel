from psycopg import AsyncConnection

from schemas.engagement_administration_profile_schemas import NewEngagementAdministrationProfile
from utils import exception_response


async def update_engagement_profile_model(
        connection: AsyncConnection,
        profile: NewEngagementAdministrationProfile,
        engagement_id: str
):
    with exception_response():
        pass


async def fetch_engagement_administration_profile_model(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        pass