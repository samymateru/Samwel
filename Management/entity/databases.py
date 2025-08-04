from Management.entity.schemas import *
from fastapi import HTTPException
from datetime import datetime
from psycopg import AsyncConnection, sql
from utils import get_unique_key, check_row_exists

async def create_new_entity(connection: AsyncConnection, entity : NewEntity):
    query = sql.SQL(
        """
        INSERT INTO public.entities (id, name, owner, email, telephone, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """)
    try:
        async with connection.cursor() as cursor:
            exists = await check_row_exists(connection=connection, table_name="entities", filters={
                "email": entity.email
            })
            print(exists)
            if exists:
                raise HTTPException(status_code=400, detail="Entity exists")
            await cursor.execute(query, (
                get_unique_key(),
                entity.name,
                entity.owner,
                entity.email,
                entity.telephone,
                datetime.now()
            ))
            entity_id = await cursor.fetchone()
            await connection.commit()
        return entity_id[0]

    except HTTPException:
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating new entity {e}")


async def get_entities(connection: AsyncConnection, entity_id: str):
    query = sql.SQL("""SELECT * FROM public.entities WHERE id = {id}""").format(id=sql.Literal(entity_id))

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying entity {e}")


async def get_entities_by_email(connection: AsyncConnection, email: str):
    query = sql.SQL("""SELECT * FROM public.entities WHERE email = {email}""").format(email=sql.Literal(email))

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying entity by email {e}")

async def get_entities_by_id(connection: AsyncConnection, user_id: str):
    query = sql.SQL("""SELECT * FROM public.entities WHERE id = %s;""")

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (user_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying entity by id {e}")

async def get_entity(connection: AsyncConnection, organization_id: str):
    query = sql.SQL(
        """
        SELECT * FROM public.organizations WHERE id = {organization_id};
        """).format(organization_id=sql.Literal(organization_id))

    query_entity = sql.SQL(
        """
        SELECT * FROM public.entities WHERE id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            organization_data = [dict(zip(column_names, row_)) for row_ in rows]
            await cursor.execute(query_entity, (organization_data[0].get("entity"),))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            entity_data = [dict(zip(column_names, row_)) for row_ in rows]
            return entity_data

    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying entity {e}")
