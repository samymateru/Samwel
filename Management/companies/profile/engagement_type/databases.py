from fastapi import HTTPException
from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.companies.profile.engagement_type.schemas import *

def new_engagement_type(connection: Connection, engagement_type: EngagementType, company_id: int):
    query: str = """
                    INSERT INTO public.engagement_types (company, name) VALUES(%s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
               company_id,
                engagement_type.name
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement type {e}")

def delete_engagement_type(connection: Connection, engagement_type_id: int):
    query: str = """
                    DELETE FROM public.engagement_types
                    WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
               engagement_type_id,
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting engagement type {e}")

def edit_engagement_type(connection: Connection, engagement_type: EngagementType, engagement_type_id: int):
    query: str = """
                    UPDATE public.engagement_types
                    SET
                    name = %s
                    WHERE id = %s 
                  """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                engagement_type.name,
                engagement_type_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating engagement type {e}")

def get_company_engagement_type(connection: Connection, company_id: int):
    query: str = """
                   SELECT * from public.engagement_types WHERE company = %s
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
        raise HTTPException(status_code=400, detail=f"Error fetching company engagement type {e}")

def get_engagement_type(connection: Connection, engagement_type_id):
    query: str = """
                    SELECT * from public.engagement_types WHERE id = %s
                  """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (engagement_type_id,))
            rows = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement type {e}")