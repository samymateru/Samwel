from psycopg import AsyncConnection
from schemas.engagement_staff_schemas import NewEngagementStaff, UpdateStaff, CreateEngagementStaff
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

        builder = ""



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