from psycopg import AsyncConnection
from core.tables import Tables
from schemas.engagement_process_schemas import NewEngagementProcess, CreateEngagementProcess, EngagementProcessColumns, \
    UpdateEngagementProcess
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key



async def create_engagement_process_model(
        connection: AsyncConnection,
        engagement_process: NewEngagementProcess,
        engagement_id: str,
        throw: bool = True
):
    with exception_response():
        __engagement_process__ = CreateEngagementProcess(
            id=get_unique_key(),
            engagement=engagement_id,
            process=engagement_process.process,
            sub_process=engagement_process.sub_process,
            description=engagement_process.description,
            business_unit=engagement_process.business_unit
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENT_PROCESS.value)
            .values(__engagement_process__)
            .check_exists({EngagementProcessColumns.PROCESS.value: engagement_process.process})
            .check_exists({EngagementProcessColumns.SUB_PROCESS.value: engagement_process.sub_process})
            .check_exists({EngagementProcessColumns.ENGAGEMENT.value: engagement_id})
            .throw_error_on_exists(throw)
            .returning(EngagementProcessColumns.ID.value)
            .execute()
        )

        return builder



async def update_engagement_process_model(
        connection: AsyncConnection,
        engagement_process: UpdateEngagementProcess,
        engagement_process_id: str
):
    with exception_response():

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ENGAGEMENT_PROCESS.value)
            .values(engagement_process)
            .check_exists({EngagementProcessColumns.ID.value: engagement_process_id})
            .where({EngagementProcessColumns.ID.value: engagement_process_id})
            .returning(EngagementProcessColumns.ID.value)
            .execute()
        )

        return builder



async def get_engagement_processes_model(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ENGAGEMENT_PROCESS.value)
            .where(EngagementProcessColumns.ENGAGEMENT.value, engagement_id)
            .fetch_all()
        )

        return builder



async def get_single_engagement_process_model(
        connection: AsyncConnection,
        engagement_process_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ENGAGEMENT_PROCESS.value)
            .where(EngagementProcessColumns.ID.value, engagement_process_id)
            .fetch_one()
        )

        return builder



async def delete_single_engagement_process_model(
        connection: AsyncConnection,
        engagement_process_id: str
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.ENGAGEMENT_PROCESS.value)
            .check_exists({EngagementProcessColumns.ID.value: engagement_process_id})
            .where({EngagementProcessColumns.ID.value: engagement_process_id})
            .returning(EngagementProcessColumns.ID.value)
            .execute()
        )

        return builder