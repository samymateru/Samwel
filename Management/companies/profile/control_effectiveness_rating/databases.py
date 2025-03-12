from fastapi import HTTPException
from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.companies.profile.control_effectiveness_rating.schemas import *

def new_control_effectiveness_rating(connection: Connection, control_effectiveness_rating: ControlEffectivenessRating, company_id: int):
    query: str = """
                    INSERT INTO public.control_effectiveness_rating (company, name) VALUES(%s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                company_id,
                control_effectiveness_rating.name
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding control_effectiveness_rating {e}")

def delete_control_effectiveness_rating(connection: Connection, control_effectiveness_rating_id: int):
    query: str = """
                        DELETE FROM public.control_effectiveness_rating
                        WHERE id = %s
                     """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                control_effectiveness_rating_id,
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting control_effectiveness_rating {e}")

def edit_control_effectiveness_rating(connection: Connection, control_effectiveness_rating: ControlEffectivenessRating, control_effectiveness_rating_id: int):
    query: str = """
                    UPDATE public.control_effectiveness_rating
                    SET
                    name = %s
                    WHERE id = %s 
                  """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                control_effectiveness_rating.name,
                control_effectiveness_rating_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating control_effectiveness_rating {e}")

def get_company_control_effectiveness_rating(connection: Connection, company_id: int):
    query: str = """
                   SELECT * from public.control_effectiveness_rating WHERE company = %s
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
        raise HTTPException(status_code=400, detail=f"Error fetching company control effectiveness rating {e}")

def get_control_effectiveness_rating(connection: Connection, control_effectiveness_rating_id):
    query: str = """
                   SELECT * from public.control_effectiveness_rating WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (control_effectiveness_rating_id,))
            rows = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching issue source {e}")