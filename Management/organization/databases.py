from psycopg import AsyncConnection, sql
from psycopg.errors import UniqueViolation

from Management.users.databases import new_user
from Management.users.schemas import Role, User
from utils import get_unique_key
from Management.organization.schemas import *
from fastapi import HTTPException

async def new_organization(connection: AsyncConnection, organization: Organization, entity_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.organization (id, entity, name, email, telephone, "default", type, status, website, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """)

    user = User(
        name=organization.owner,
        email=organization.email,
        telephone=organization.telephone,
        title="Owner",
        role=[Role(name="Admin")],
        module=[],
        status=True
    )

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                get_unique_key(),
                entity_id,
                organization.name,
                organization.email,
                organization.telephone,
                organization.default,
                organization.type,
                organization.status,
                organization.website,
                datetime.now()
            ))
            organization_id = await cursor.fetchone()
            await new_user(connection=connection, user=user, organization_id=[organization_id[0]])
            await connection.commit()
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail=" already already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating new organization {e}")

async def update_organization(connection: AsyncConnection, organization: Organization, organization_id: str):
    pass

async def fetch_organizations(connection: AsyncConnection, company_id: str):
    pass

async def fetch_organization(connection: AsyncConnection, company_id: str):
    pass