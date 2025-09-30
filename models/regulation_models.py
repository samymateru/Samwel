from psycopg import AsyncConnection
from core.tables import Tables
from schemas.regulation_schemas import NewRegulation, CreateRegulation, RegulationColumns, UpdateRegulation
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key


async def create_new_regulation_model(
        connection: AsyncConnection,
        regulation: NewRegulation,
        engagement_id: str
):
    with exception_response():
        __regulation__ = CreateRegulation(
            id=get_unique_key(),
            engagement=engagement_id,
            name=regulation.name,
            issue_date=regulation.issue_date,
            key_areas=regulation.key_areas
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.REGULATIONS.value)
            .values(__regulation__)
            .check_exists({RegulationColumns.NAME.value: regulation.name})
            .returning(RegulationColumns.ID.value)
            .execute()
        )

        return builder



async def get_engagement_regulations_model(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.REGULATIONS.value)
            .where(RegulationColumns.ENGAGEMENT.value, engagement_id)
            .fetch_all()
        )

        return builder


async def get_single_engagement_regulation_model(
        connection: AsyncConnection,
        regulation_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.REGULATIONS.value)
            .where(RegulationColumns.ID.value, regulation_id)
            .fetch_one()
        )

        return builder


async def update_engagement_regulation_model(
        connection: AsyncConnection,
        regulation: UpdateRegulation,
        regulation_id: str
):
    with exception_response():
        __regulation__ = UpdateRegulation(
            name=regulation.name,
            issue_date=regulation.issue_date,
            key_areas=regulation.key_areas
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.REGULATIONS.value)
            .values(__regulation__)
            .check_exists({RegulationColumns.ID.value: regulation_id})
            .where({RegulationColumns.ID.value: regulation_id})
            .returning(RegulationColumns.ID.value)
            .execute()
        )

        return builder


async def delete_engagement_regulation_model(
        connection: AsyncConnection,
        regulation_id: str
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.REGULATIONS.value)
            .check_exists({RegulationColumns.ID.value: regulation_id})
            .where({RegulationColumns.ID.value: regulation_id})
            .returning(RegulationColumns.ID.value)
            .execute()
        )

        return builder
