from psycopg import AsyncConnection
from utils import exception_response


async def load_issue_finding(
    connection: AsyncConnection,
    engagement_id: str
):
    with exception_response():
        pass