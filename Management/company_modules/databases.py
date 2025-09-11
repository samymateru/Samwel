import json
from fastapi import HTTPException
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from Management.company_modules.schemas import *
from psycopg import AsyncConnection, sql
from Management.users.schemas import UserType
from utils import get_unique_key, check_row_exists


async def add_new_organization_module(
        connection: AsyncConnection,
        module: Module,
        organization_id: str,
):
    query = sql.SQL(
        """
        INSERT INTO public.modules 
        (
         id,
         organization, 
         name, 
         purchase_date, 
         status
         )
        VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """)
    try:
        async with connection.cursor() as cursor:
            exists = await check_row_exists(connection=connection, table_name="modules", filters={
                "name": module.name,
                "organization": organization_id
            })
            if exists:
                raise HTTPException(status_code=400, detail="Module exists")
            await cursor.execute(query,(
                module.id,
                organization_id,
                module.name,
                module.purchase_date,
                module.status
            ))
            module_id = await cursor.fetchone()
            await connection.commit()
            return module_id[0]
    except HTTPException as e:
        await connection.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating organization module {e}")

async def get_users_modules(connection: AsyncConnection, user_id: str, organization_id: str):
    query = sql.SQL(
        """
        SELECT
        mod.id, 
        mod.name,
        mod.purchase_date,
        mod.status,
        mod_usr.role,
        mod_usr.title,
        mod_usr.type
        FROM modules mod
        JOIN organizations org ON mod.organization = org.id
        JOIN modules_users mod_usr ON mod.id = mod_usr.module_id
        WHERE mod_usr.user_id = %s AND org.id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (user_id, organization_id))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            modules_data = [dict(zip(column_names, row_)) for row_ in rows]
            return modules_data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying company modules {e}")

async def get_risk_module_users(connection: AsyncConnection, user_id: str, organization_id: str):
    query = sql.SQL(
        """
        SELECT
        mod.id, 
        mod.name,
        mod.purchase_date,
        mod.status,
        mod_usr.role,
        mod_usr.type
        FROM modules mod
        JOIN organizations org ON mod.organization = org.id
        JOIN risk_module_users mod_usr ON mod.id = mod_usr.module_id
        WHERE mod_usr.user_id = %s AND org.id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (user_id, organization_id))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            modules_data = [dict(zip(column_names, row_)) for row_ in rows]
            return modules_data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying company modules {e}")


async def get_organization_modules(connection: AsyncConnection, organization_id: str):
    query = sql.SQL(
        """
        SELECT 
        mod.id, 
        mod.name, 
        mod.purchase_date, 
        mod.status
        FROM public.modules mod
        WHERE mod.organization = %s;
        """)
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
