from psycopg import AsyncConnection, sql
from utils import check_row_exists, check_row_count, check_if_entity_administrator
from Management.organization.schemas import *
from fastapi import HTTPException

async def create_organization(connection: AsyncConnection, organization: Organization,  entity_id: str, user_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.organizations (id, entity, name, email, telephone, "default", type, status, state, website, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """)

    try:
        async with connection.cursor() as cursor:
            exists = await check_row_exists(connection=connection, table_name="organizations", filters={
                "name": organization.name,
                "entity": entity_id
            })
            if exists:
                raise HTTPException(status_code=400, detail="Organization exists")

            await check_if_entity_administrator(connection=connection, user_id=user_id)
            await cursor.execute(query, (
            organization.id,
            entity_id,
            organization.name,
            organization.email,
            organization.telephone,
            organization.default,
            organization.type,
            organization.status,
            "active",
            organization.website,
            datetime.now()
            ))
            organization_id = await cursor.fetchone()
            await connection.commit()
            return organization_id[0]
    except HTTPException:
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating new organization {e}")


async def get_user_organizations(connection: AsyncConnection, user_id: str):
    query = sql.SQL(
        """
        SELECT
        org.id,
        org.name,
        org.email,
        org.telephone,
        org.default,
        org.type,
        org.status,
        org.website,
        org_user.administrator,
        org_user.owner
        FROM public.organizations_users as org_user
        JOIN organizations org ON org.id = org_user.organization_id
        WHERE user_id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (user_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            organization_data = [dict(zip(column_names, row_)) for row_ in rows]
            return organization_data
    except HTTPException as e:
        await connection.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying user {e}")


async def update_organization(connection: AsyncConnection, organization: Organization, organization_id: str):
    query = sql.SQL(
        """
        UPDATE public.organizations
        SET 
        name = %s,
        email = %s,
        telephone = %s,
        type = %s
        WHERE id = %s
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query,(
                organization.name,
                organization.email,
                organization.telephone,
                organization.type,
                organization_id
            ))
            await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating organization {e}")

async def get_organization_data(connection: AsyncConnection, organization_id: str):
    query = sql.SQL(
        """
        SELECT * FROM public.organizations WHERE id = {id}
        """).format(id=sql.Literal(organization_id))
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            organization_data = [dict(zip(column_names, row_)) for row_ in rows]
            return organization_data
    except HTTPException as e:
        await connection.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error organization data {e}")

async def trash_organizations(connection: AsyncConnection, organization_id: str):
    query = sql.SQL(
        """
        UPDATE public.organizations
        SET 
        state = 'inactive'
        WHERE id = %s;
        """)

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query=query, params=(organization_id,))
            await check_row_count(cursor=cursor, detail="Error organization not found")
            await connection.commit()

    except HTTPException:
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting organization {e}")
