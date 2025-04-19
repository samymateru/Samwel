import json
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
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

def delete_user(connection: Connection, user_id: str) -> None:
    query = """
               DELETE FROM public.users
               WHERE id = %s
               RETURNING id;
               """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (user_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error deleting the user {e}")
        raise HTTPException(status_code=400, detail="Error deleting the user")

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

def get_roles_ids(connection: Connection, user_id: int):
    query = "SELECT role_id FROM public.users WHERE id = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        print(f"Error querying users roles id {e}")
        raise HTTPException(status_code=400, detail="Error querying users")


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
        raise HTTPException(status_code=400, detail=f"Error adding module")







# older implementation
# def new_user_(connection: Connection, user_data: NewUser, company_id: int):
#     query = """
#                INSERT INTO public.users (company, name, telephone, email,
#                type, module, role, password_hash, status, created_at)
#                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
#                """
#     try:
#         with connection.cursor() as cursor:
#             cursor: Cursor
#             cursor.execute("SELECT 1 FROM public.users WHERE email = %s", (user_data.email,))
#             if cursor.fetchone():
#                 raise ValueError("User already exists")
#             else:
#                 cursor.execute(query,
#                                (
#                                    company_id,
#                                    user_data.name,
#                                    user_data.telephone,
#                                    user_data.email,
#                                    user_data.type,
#                                    '[]',
#                                    json.dumps(user_data.model_dump().get("role")),
#                                    generate_hash_password(user_data.password),
#                                    user_data.status,
#                                    datetime.now()
#                                ))
#                 connection.commit()
#             return cursor.fetchone()[0]
#     except ValueError as v:
#         raise HTTPException(status_code=401, detail="user exists")
#     except Exception as e:
#         connection.rollback()
#         raise HTTPException(status_code=400, detail=f"Error creating new user {e}")
#
# def get_user_(connection: Connection, column: str, value: int | str):
#     query = "SELECT * FROM public.users "
#     if column and value:
#         query += f"WHERE  {column} = %s"
#
#     try:
#         with connection.cursor() as cursor:
#             cursor: Cursor
#             cursor.execute(query, (value,))
#             rows = cursor.fetchall()
#             column_names = [desc[0] for desc in cursor.description]
#             data = [dict(zip(column_names, row_)) for row_ in rows]
#             return data
#     except Exception as e:
#         connection.rollback()
#         raise HTTPException(status_code=400, detail=f"Error querying users {e}")