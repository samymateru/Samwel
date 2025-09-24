from psycopg import AsyncConnection
from core.tables import Tables
from schemas.entity_schemas import NewEntity, CreateEntity, EntitiesColumns
from services.connections.postgres.insert import InsertQueryBuilder
from utils import exception_response, get_unique_key
from datetime import datetime

async def register_new_entity(connection: AsyncConnection, entity: NewEntity):
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

