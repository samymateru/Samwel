from psycopg import AsyncConnection
from datetime import datetime
from core.tables import Tables
from schemas.management_schemas import NewManagement, CreatedManagement, ManagementColumns, UpdateManagement
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key


async def create_new_management_model(
        connection: AsyncConnection,
        organization_id: str,
        management: NewManagement
):
    with exception_response():
        __create_organization__ = CreatedManagement(
            management_id=get_unique_key(),
            organization_id=organization_id,
            name=management.name,
            email=management.email,
            title=management.title,
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.MANAGEMENT.value)
            .values(__create_organization__)
            .check_exists({ManagementColumns.EMAIL.value: management.email})
            .check_exists({ManagementColumns.NAME.value: management.name})
            .returning(ManagementColumns.MANAGEMENT_ID.value)
            .execute()
        )

        return builder



async def fetch_organization_management_model(
        connection: AsyncConnection,
        organization_id: str,
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.MANAGEMENT.value)
            .where(ManagementColumns.ORGANIZATION_ID.value, organization_id)
            .fetch_all()
        )

        return builder



async def update_organization_management_model(
        connection: AsyncConnection,
        management: UpdateManagement,
        management_id: str,
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.MANAGEMENT.value)
            .values(management)
            .check_exists({ManagementColumns.MANAGEMENT_ID.value: management_id})
            .where({ManagementColumns.MANAGEMENT_ID.value: management_id})
            .returning(ManagementColumns.MANAGEMENT_ID.value)
            .execute()
        )

        return builder



async def delete_organization_management_model(
        connection: AsyncConnection,
        management_id: str,
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.MANAGEMENT.value)
            .check_exists({ManagementColumns.MANAGEMENT_ID.value: management_id})
            .where({ManagementColumns.MANAGEMENT_ID.value: management_id})
            .returning(ManagementColumns.MANAGEMENT_ID.value)
            .execute()
        )

        return builder