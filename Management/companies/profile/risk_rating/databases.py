from fastapi import HTTPException
from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.companies.profile.risk_rating.schemas import *

def new_risk_rating(connection: Connection, risk_rating: RiskRating, company_id: int):
    query: str = """
                    INSERT INTO public.risk_rating (company, name, magnitude) VALUES(%s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                company_id,
                risk_rating.name,
                risk_rating.magnitude
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding risk rating {e}")

def delete_risk_rating(connection: Connection, risk_rating_id: int):
    query: str = """
                    DELETE FROM public.risk_rating
                    WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
               risk_rating_id,
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting risk rating {e}")

def edit_risk_rating(connection: Connection, risk_rating: RiskRating, risk_rating_id: int):
    query: str = """
                    UPDATE public.risk_rating
                    SET
                    name = %s,
                    magnitude = %s
                    WHERE id = %s 
                  """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                risk_rating.name,
                risk_rating.magnitude,
                risk_rating_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating risk rating {e}")

def get_company_risk_rating(connection: Connection, company_id: int):
    query: str = """
                   SELECT * from public.risk_rating WHERE company = %s
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
        raise HTTPException(status_code=400, detail=f"Error fetching company risk rating {e}")

def get_risk_rating(connection: Connection, risk_rating_id):
    query: str = """
                   SELECT * from public.risk_rating WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (risk_rating_id,))
            rows = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching risk rating{e}")