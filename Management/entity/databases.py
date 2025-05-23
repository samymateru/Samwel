from psycopg.errors import UniqueViolation
from Management.entity.schemas import *
from fastapi import HTTPException
from datetime import datetime
from psycopg import AsyncConnection, sql
from Management.organization.databases import new_organization
from Management.organization.schemas import Organization, OrganizationStatus
from redis_cache import cached
from utils import get_unique_key

async def create_new_entity(connection: AsyncConnection, entity : NewEntity):
    query = sql.SQL(
        """
        INSERT INTO public.entity (id, name, owner, email, telephone, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """)

    organization = Organization(
        name=entity.name,
        owner=entity.owner,
        email=entity.email,
        telephone=entity.telephone,
        type=entity.type,
        website=entity.website,
        status=OrganizationStatus.OPENED.value,
        default=True,
        created_at=datetime.now()
    )

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                get_unique_key(),
                entity.name,
                entity.owner,
                entity.email,
                entity.telephone,
                datetime.now()
            ))
            entity_id = await cursor.fetchone()
            await new_organization(connection=connection, organization=organization, entity_id=entity_id[0])
            await connection.commit()
        return entity_id[0]
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Entity already already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating new entity {e}")

@cached(ttl=60*60)
async def get_entities(connection: AsyncConnection, entity_id: str):
    query = sql.SQL("""SELECT * FROM public.entity WHERE id = %s""")

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (entity_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying entity {e}")
