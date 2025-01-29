from typing import Tuple, List, Dict
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from Management.modules.schemas import UpdateModule, NewModule
from fastapi import HTTPException
from datetime import datetime

def create_new_module(connection: Connection, module_data: NewModule, company_id: int):
    query = """
               INSERT INTO public.modules (company_id, name, description, status, created_at) 
               VALUES (%s, %s, %s, %s, %s)
               """
    query_check = "SELECT 1 FROM public.modules WHERE name = %s AND company_id = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query_check, (module_data.name, company_id,))
            if cursor.fetchone():
                raise HTTPException(status_code=409, detail="Module already exists")
            cursor.execute(query, (
                                company_id,
                                module_data.name,
                                module_data.description,
                                module_data.status,
                                datetime.now()
                                ))
        connection.commit()
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        print(f"Error creating module {e}")
        raise HTTPException(status_code=500, detail="Error creating module")

def update_module(connection: Connection, module_data: UpdateModule) -> None:
    query_parts = []
    params = []

    # Check if the description is set
    if module_data.description is not None:
        query_parts.append("description = %s")
        params.append(module_data.description)

    # If no fields to update, raise an error and return
    if not query_parts:
        raise HTTPException(status_code=400, detail="No fields to update")
    # query_parts.append("updated_at = %s")
    # params.append(datetime.now())
    # Construct the SET part without trailing commas
    set_clause = ", ".join(query_parts)

    # Add the WHERE condition
    where_clause = "WHERE id = %s"
    params.append(module_data.id)

    # Combine the SET and WHERE parts into the final query
    query = f"UPDATE public.modules SET {set_clause} {where_clause}"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, tuple(params))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error updating module {e}")
        raise HTTPException(status_code=400, detail="Error updating module")


def delete_module(connection: Connection, module_id: str) -> None:
    query = """
               DELETE FROM public.modules WHERE id = %s RETURNING id;
               """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (module_id, ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error deleting module {e}")
        raise HTTPException(status_code=400, detail="Error deleting module")

def get_modules(connection: Connection, column: str = None, value: str = None, row: str = None) -> List[Dict]:
    query = "SELECT * FROM public.modules "
    if row:
        query = f"SELECT {row} FROM public.modules "
    if column and value:
        query += f"WHERE  {column} = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        print(f"Error querying modules {e}")
        raise HTTPException(status_code=400, detail="Error querying modules")

def get_active_modules(connection: Connection, module_ids: List[int]):
    query = "SELECT * FROM public.modules WHERE id = ANY(%s);"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (module_ids,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        print(f"Error querying modules {e}")
        raise HTTPException(status_code=400, detail="Error querying modules")