from psycopg import AsyncConnection
from AuditNew.Internal.follow_up.schemas import NewFollowUp, CreateFollowUp, FollowUpStatus, FollowUpColumns
from services.connections.postgres.insert import InsertQueryBuilder
from utils import exception_response, get_unique_key
from datetime import datetime


async def add_new_follow_up(connection: AsyncConnection, follow_up: NewFollowUp, module_id: str, user_id: str):
    with exception_response():
        __follow_up__ = CreateFollowUp(
            follow_up_id=get_unique_key(),
            name=follow_up.name,
            module_id=module_id,
            status=FollowUpStatus.DRAFT,
            created_at=datetime.now(),
            created_by=user_id,
        )
        builder =  await (
            InsertQueryBuilder(connection=connection)
            .into_table("follow_up")
            .values(__follow_up__)
            .returning(FollowUpColumns.FOLLOW_UP_ID.value)
            .execute()
        )
        return builder

