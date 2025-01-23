from typing import Tuple, List, Dict
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from Management.company_modules.schemas import UpdateCompanyModule
from datetime import datetime

def create_new_company_module(connection: Connection, company_module_data: Tuple) -> None:
    query = """
            INSERT INTO public.roles (company_id, module_id, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
            """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, company_module_data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error creating company module {e}")
        raise HTTPException(status_code=400, detail="Error creating company module")

def update_company_module(connection: Connection, company_module_data: UpdateCompanyModule) -> None:
    query_parts = []
    params = []

    #Check if the module  is set
    if company_module_data.module_id is not None:
        query_parts.append("module_id = %s")
        params.append(company_module_data.module_id)

    # Check if the is active is set
    if company_module_data.is_active is not None:
        query_parts.append("is_active = %s")
        params.append(company_module_data.is_active)

    # If no fields to update, raise an error and return
    if not query_parts:
        raise HTTPException(status_code=400, detail="No fields to update")

    query_parts.append("updated_at = %s")
    params.append(datetime.now())

    # Construct the SET part without trailing commas
    set_clause = ", ".join(query_parts)

    # Add the WHERE condition
    where_clause = "WHERE company_module_id = %s"
    params.append(company_module_data.company_module_id)

    # Combine the SET and WHERE parts into the final query
    query = f"UPDATE public.company_modules SET {set_clause} {where_clause}"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, tuple(params))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error updating company module {e}")
        raise HTTPException(status_code=400, detail="Error updating company module ")


def delete_company_module(connection: Connection, company_module_id: List[int]) -> None:
    query = """
            DELETE FROM public.company_modules
            WHERE company_module_id = ANY(%s)
            RETURNING company_module_id;
            """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (company_module_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error deleting company module {e}")
        raise HTTPException(status_code=400, detail="Error deleting company module")

def get_company_modules(connection: Connection, column: str = None, value: str = None, row: str = None) -> List[Dict]:
    query = "SELECT * FROM public.company_modules "
    if row:
        query = f"SELECT {row} FROM public.company_modules "
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
        print(f"Error querying company modules {e}")
        raise HTTPException(status_code=400, detail="Error querying company modules")