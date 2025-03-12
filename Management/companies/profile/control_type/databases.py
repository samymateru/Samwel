from fastapi import HTTPException
from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.companies.profile.control_type.schemas import *

def new_control_type(connection: Connection, control_type: ControlType, company_id: int):
    query: str = """
                    INSERT INTO public.control_type (company, name) VALUES(%s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                company_id,
                control_type.name
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding control type {e}")

def delete_control_type(connection: Connection, control_type_id: int):
    query: str = """
                        DELETE FROM public.control_type
                        WHERE id = %s
                     """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                control_type_id,
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting control type {e}")

def edit_control_type(connection: Connection, control_type: ControlType, control_type_id: int):
    query: str = """
                    UPDATE public.control_type
                    SET
                    name = %s
                    WHERE id = %s 
                  """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                control_type.name,
                control_type_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating control type {e}")

def get_company_control_type(connection: Connection, company_id: int):
    query: str = """
                   SELECT * from public.control_type WHERE company = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (company_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching company control type {e}")

def get_control_type(connection: Connection, control_type_id):
    query: str = """
                   SELECT * from public.control_type WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (control_type_id,))
            rows = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching control type {e}")