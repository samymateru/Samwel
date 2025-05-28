from psycopg import AsyncConnection, sql
from psycopg.errors import UniqueViolation

from Management.users.databases import new_user
from Management.users.schemas import User
from utils import get_unique_key
from Management.organization.schemas import *
from fastapi import HTTPException

async def new_organization(connection: AsyncConnection, organization: Organization, entity_id: str, default: bool = False):
    query = sql.SQL(
        """
        INSERT INTO public.organization (id, entity, name, email, telephone, "default", type, status, website, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """)

    user = User(
        name=organization.name,
        email=organization.email,
        telephone=organization.telephone,
        module_id=[]
    )

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
            get_unique_key(),
            entity_id,
            organization.name,
            organization.email,
            organization.telephone,
            default,
            organization.type,
            "Opened",
            organization.website,
            datetime.now()
            ))
            organization_id = await cursor.fetchone()
            await new_user(connection=connection, user=user, organization_id=organization_id[0])
            await connection.commit()
            return organization_id[0]

    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail=" already already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating new organization {e}")


async def get_user_organizations(connection: AsyncConnection, user_id: str):
    query = sql.SQL(
        """
        SELECT * FROM public.organization WHERE id = ANY(%s);
        """)
    organization_list_query = sql.SQL(
        """
        SELECT organization FROM public.users WHERE id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(organization_list_query, (user_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            user_organizations = [dict(zip(column_names, row_)) for row_ in rows]
            if user_organizations.__len__() == 0:
                raise HTTPException(status_code=400, detail="User not exists")
            await cursor.execute(query, (user_organizations[0].get("organization"),))
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
