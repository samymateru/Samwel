from typing import Tuple
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from typing import List, Dict
from Management.users.schemas import UpdateUser, NewUser
from fastapi import HTTPException
from datetime import datetime
from utils import generate_hash_password
from Management.roles import databases as roles_database

def create_new_user(connection: Connection, user_data: NewUser, company_id: int) -> None:
    query = """
               INSERT INTO public.users (company_id, name, telephone, email,
               type, role_id, password_hash, status, created_at) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                                   user_data.role_id,
                                   generate_hash_password(user_data.password),
                                   user_data.status,
                                   datetime.now()
                               ))
                connection.commit()
    except ValueError as v:
        raise HTTPException(status_code=401, detail="user exists")
    except Exception as e:
        connection.rollback()
        print(f"Error creating new user {e}")
        raise HTTPException(status_code=400, detail="Error creating new user")



def update_user(connection: Connection, user_data: UpdateUser) -> None:
    query_parts = []
    params = []

    # Check if the first_name is set
    if user_data.name is not None:
        query_parts.append("name = %s")
        params.append(user_data.name)

    # Check if the telephone date is set
    if user_data.telephone is not None:
        query_parts.append("telephone = %s")
        params.append(user_data.telephone)

    # Check if the  type is set
    if user_data.type is not None:
        query_parts.append("type = %s")
        params.append(user_data.type)

    # Check if the  email is set
    if user_data.email is not None:
        query_parts.append("email = %s")
        params.append(user_data.email)

    # Check if the  is active is set
    if user_data.status is not None:
        query_parts.append("status = %s")
        params.append(user_data.status)

    # Check if the  role is set
    if user_data.role is not None:
        query_parts.append("role = %s")
        params.append(user_data.role)

    # If no fields to update, raise an error and return
    if not query_parts:
        raise HTTPException(status_code=400, detail="No fields to update")

    # query_parts.append("updated_at = %s")
    # params.append(datetime.now())

    set_clause = ", ".join(query_parts)
    # Add the WHERE condition
    where_clause = "WHERE id = %s"
    params.append(user_data.id)

    # Combine the SET and WHERE parts into the final query
    query = f"UPDATE public.users SET {set_clause} {where_clause}"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, tuple(params))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error updating the user {e}")
        raise HTTPException(status_code=400, detail="Error updating the user")

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

def get_user(connection: Connection, column: str = None, value: str | int = None, row: List[str] = None) -> List[Dict]:
    query = "SELECT * FROM public.users "
    if row:
        query = f"SELECT {" ,".join(row)} FROM public.users "
    if column and value:
        query += f"WHERE  {column} = %s"

    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            for i in data:
                roles = roles_database.get_user_roles(connection, i.get("role_id"))
                i["roles"] = roles  # Add the roles to the current row dictionary
            return data
    except Exception as e:
        connection.rollback()
        print(f"Error querying users {e}")
        raise HTTPException(status_code=400, detail="Error querying users")

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
    pass



