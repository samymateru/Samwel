from fastapi import HTTPException
from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.companies.profile.control_weakness_rating.schemas import *

def new_control_weakness_rating(connection: Connection,control_weakness_rating: ControlWeaknessRating, company_id: int):
    query: str = """
                    INSERT INTO public.control_weakness_rating (company, name) VALUES(%s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
               company_id,
                control_weakness_rating.name
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding control weakness rating {e}")

def delete_control_weakness_rating(connection: Connection, control_weakness_rating_id: int):
    query: str = """
                    DELETE FROM public.control_weakness_rating
                    WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
               control_weakness_rating_id,
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting control weakness rating {e}")

def edit_control_weakness_rating(connection: Connection, control_weakness_rating: ControlWeaknessRating, control_weakness_rating_id: int):
    query: str = """
                    UPDATE public.control_weakness_rating
                    SET
                    name = %s
                    WHERE id = %s 
                  """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                control_weakness_rating.name,
                control_weakness_rating_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating control weakness rating {e}")

def get_company_control_weakness_rating(connection: Connection, company_id: int):
    query: str = """
                   SELECT * from public.control_weakness_rating WHERE company = %s
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
        raise HTTPException(status_code=400, detail=f"Error fetching company control weakness rating {e}")

def get_control_weakness_rating(connection: Connection, control_weakness_rating_id):
    query: str = """
                   SELECT * from public.control_weakness_rating WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (control_weakness_rating_id,))
            rows = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching control weakness rating {e}")