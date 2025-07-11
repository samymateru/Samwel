import json
from fastapi import HTTPException
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from Management.company_modules.schemas import *
from psycopg import AsyncConnection, sql
from Management.users.schemas import UserType
from utils import get_unique_key

async def add_new_organization_module(
        connection: AsyncConnection,
        organization_module: Module,
        organization_id: str,
        user_id: str
):
    query = sql.SQL(
        """
        INSERT INTO public.modules (id, organization, name, purchase_date, status)
        VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """)

    check_module_query = sql.SQL(
        """
        SELECT id FROM public.modules WHERE name = {name} AND organization = {organization}
        """).format(
        name=sql.Literal(organization_module.name),
        organization=sql.Literal(organization_id)
    )

    update_user_query = sql.SQL(
        """
        UPDATE public.modules 
        SET users = %s::jsonb
        WHERE id = %s
        """)

    user_type = UserType(
        id=user_id,
        type="audit",
        role="Administrator",
        title="Administrator",
        engagements=[]
    )

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(check_module_query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            module_data = [dict(zip(column_names, row_)) for row_ in rows]
            if module_data.__len__() == 0:
                await cursor.execute(query,(
                    get_unique_key(),
                    organization_id,
                    organization_module.name,
                    organization_module.purchase_date,
                    organization_module.status
                ))
                module_id = await cursor.fetchone()
                await cursor.execute(update_user_query, (json.dumps([user_type.model_dump()]), module_id[0]))
                await connection.commit()
                return module_id[0]
            else:
                raise HTTPException(status_code=400, detail="Module exists in this organization")
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Invalid company id")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Company module already exist")
    except HTTPException as e:
        await connection.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating organization module {e}")

async def get_users_modules(connection: AsyncConnection, user_id: str):
    query = sql.SQL(
        """
        SELECT * FROM public.modules WHERE id = ANY(%s)
        """)

    check_user_query = sql.SQL(
        """
        SELECT modules FROM public.users WHERE id = {user_id}
        """).format(user_id=sql.Literal(user_id))
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(check_user_query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            user_data = [dict(zip(column_names, row_)) for row_ in rows]
            await cursor.execute(query, (user_data[0].get("modules"), ))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            module_data = [dict(zip(column_names, row_)) for row_ in rows]
            return module_data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying company modules {e}")

async def get_organization_modules(connection: AsyncConnection, organization_id: str):
    query = sql.SQL("SELECT id, name, purchase_date, status, users FROM public.modules WHERE organization = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (organization_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying organization modules {e}")

async def delete_company_module(connection: AsyncConnection, company_module_id: str):
    query = sql.SQL("""
            DELETE FROM public.company_modules
            WHERE company_module_id = ANY(%s)
            RETURNING company_module_id;
            """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_module_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting company module {e}")

async def get_company_modules(connection: AsyncConnection, company_id: str):
    query = sql.SQL("SELECT * FROM public.company_modules WHERE company = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying company modules {e}")
