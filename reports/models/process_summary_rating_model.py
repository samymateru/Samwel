from psycopg import AsyncConnection
from AuditNew.Internal.engagements.reporting.databases import get_summary_audit_process
from utils import exception_response


async def process_summary_rating_model(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        data = await get_summary_audit_process(
            connection=connection,
            engagement_id=engagement_id
        )

        return data

