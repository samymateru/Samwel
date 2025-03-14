import json
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from fastapi import HTTPException
from utils import generate_hash_password
from Management.users.schemas import *

def new_user(connection: Connection, user_data: NewUser, company_id: int) -> None:
    query = """
               INSERT INTO public.users (company, name, telephone, email,
               type, role, module, password_hash, status, created_at) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute("SELECT 1 FROM public.users WHERE email = %s", (user_data.email,))
            if cursor.fetchone():
                raise ValueError("User already exists")
            else:
                cursor.execute(query,
                               (
                                   company_id,
                                   user_data.name,
                                   user_data.telephone,
                                   user_data.email,
                                   user_data.type,
                                   json.dumps(user_data.role),
                                   json.dumps(user_data.module),
                                   generate_hash_password(user_data.password),
                                   user_data.status,
                                   datetime.now()
                               ))
                connection.commit()
    except ValueError as v:
        raise HTTPException(status_code=401, detail="user exists")
    except Exception as e:
        connection.rollback()
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

def get_user(connection: Connection, column: str, value: int | str):
    query = "SELECT * FROM public.users "
    if column and value:
        query += f"WHERE  {column} = %s"

    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying users {e}")

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

def add_role(connection: Connection, user_id: int, role_id: int):
    query = """UPDATE public.users SET role_id = array_append(role_id, %s) WHERE NOT (%s = ANY(role_id)) AND id = %s;"""
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (role_id, role_id, user_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error add role to a user {e}")
        raise HTTPException(status_code=400, detail="Error adding role")

def remove_role(connection: Connection, user_id: int, role_id: int):
    query = """UPDATE public.users SET role_id = array_remove(role_id, %s) WHERE id = %s; """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (role_id, user_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error add role to a user {e}")
        raise HTTPException(status_code=400, detail="Error adding role")


def add_user_module(connection: Connection, module: Module, user_id: int):
    query: str = """
                  UPDATE public.users SET 
                  module = %s::jsonb
                  WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                module.model_dump_json(),
                user_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding module")



