from psycopg import AsyncConnection
from core.tables import Tables
from schemas.entity_schemas import NewEntity, CreateEntity, EntitiesColumns
from schemas.organization_schemas import OrganizationsColumns
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from utils import exception_response, get_unique_key
from datetime import datetime

async def register_new_entity(
        connection: AsyncConnection,
        entity: NewEntity
):
    with exception_response():
        __entity__ = CreateEntity(
            id=get_unique_key(),
            name=entity.name,
            owner=entity.owner,
            email=entity.email,
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ENTITIES)
            .values(__entity__)
            .check_exists({EntitiesColumns.EMAIL.value: entity.email})
            .returning(EntitiesColumns.ID.value)
            .execute()
        )

        return builder

async def get_entity_details(
        connection: AsyncConnection,
        entity_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ENTITIES.value)
            .where(EntitiesColumns.ID.value, entity_id)
            .fetch_one()
        )

        return builder

async def get_organization_entity_details(
        connection: AsyncConnection,
        organization_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ORGANIZATIONS.value, alias="org")
            .where(OrganizationsColumns.ID.value, organization_id)
            .join(
                "LEFT",
                Tables.ENTITIES.value,
                "enty.id = org.entity",
                alias="enty",
                use_prefix=False
            )
            .fetch_one()
        )

        return builder