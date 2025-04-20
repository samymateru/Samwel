import json
from fastapi import HTTPException
from Management.roles.schemas import *
from psycopg import AsyncConnection, sql


async def get_roles(connection: AsyncConnection, company_id: str):
    query = sql.SQL("SELECT * FROM public.roles WHERE company = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying roles {e}")

async def add_role(connection: AsyncConnection, role: Category, company_id: str):
    query = sql.SQL(
        """
          UPDATE public.roles
          SET roles = roles || %s::jsonb
          WHERE company = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (role.model_dump_json(), company_id))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating roles {e}")

async def edit_role(connection: AsyncConnection, role: Category, company_id: str, name: str):
    query = sql.SQL("""
                   UPDATE roles
                   SET roles = %s::jsonb
                   WHERE company = %s;
                 """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT roles FROM roles WHERE company = %s;", (company_id,))
            result = await cursor.fetchone()
            if not result:
                raise HTTPException(status_code=203, detail="No roles")
            roles = result[0]
            for role_ in roles:
                if role_["name"] == name:
                    role_["name"] = role.name  # Update the role name
                    role_["permissions"] = role.permissions.model_dump()  # Update permissions
                    break
            await cursor.execute(query, (json.dumps(roles), company_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating roles {e}")


