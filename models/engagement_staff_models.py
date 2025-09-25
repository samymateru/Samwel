from psycopg import AsyncConnection
from schemas.engagement_staff_schemas import NewEngagementStaff, UpdateStaff
from utils import exception_response


async def create_new_engagement_staff_model(
        connection: AsyncConnection,
        staff: NewEngagementStaff,
        engagement_id: str,
):
    with exception_response():
        pass


async def fetch_engagement_staff_model(
        connection: AsyncConnection,
        engagement_id: str,
):
    with exception_response():
        pass


async def update_staff_model(
        connection: AsyncConnection,
        staff: UpdateStaff,
        staff_id: str,
):
    with exception_response():
        pass


async def delete_staff_model(
        connection: AsyncConnection,
        staff_id: str,
):
    with exception_response():
        pass