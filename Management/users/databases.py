import json
from fastapi import HTTPException
from utils import generate_hash_password
from Management.users.schemas import *
from psycopg import AsyncConnection, sql
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from utils import get_unique_key

async def new_user(connection: AsyncConnection, user_: NewUser, company_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.users (id, company, name, telephone, email,
        type, module, role, password_hash, status, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query,
                                 (
                                     get_unique_key(),
                                     company_id,
                                     user_.name,
                                     user_.telephone,
                                     user_.email,
                                     user_.type,
                                     '[]',
                                     json.dumps(user_.model_dump().get("role")),
                                     generate_hash_password(user_.password),
                                     user_.status,
                                     datetime.now()
                                 ))
            user_id = await cursor.fetchone()
            await connection.commit()
            return user_id[0]
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Invalid company id")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="User already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating new user {e}")

async def delete_user(connection: AsyncConnection, user_id: str):
    query = sql.SQL("DELETE FROM public.users WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (user_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting the user {e}")

async def get_user(connection: AsyncConnection, user_id: str):
    query = sql.SQL("SELECT * FROM public.users WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (user_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying user {e}")

async def get_users(connection: AsyncConnection, company_id: str):
    query = sql.SQL("SELECT * FROM public.users WHERE company = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying users {e}")

async def get_user_by_email(connection: AsyncConnection, email: str):
    query = sql.SQL("SELECT * FROM public.users WHERE email = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (email,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying users by email {e}")

async def add_user_module(connection: AsyncConnection, module: Module, user_id: str):
    query = sql.SQL(
        """
        UPDATE public.users SET 
        module = module || %s::jsonb
        WHERE id = %s
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                module.model_dump_json(),
                user_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding module {e}")

