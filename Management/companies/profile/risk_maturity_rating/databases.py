from fastapi import HTTPException
from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.companies.profile.risk_maturity_rating.schemas import *

def new_risk_maturity_rating(connection: Connection, maturity_rating: RiskMaturityRating, company_id: int):
    query: str = """
                    INSERT INTO public.risk_maturity_rating (company, name) VALUES(%s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
               company_id,
                maturity_rating.name
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding risk maturity rating {e}")

def delete_risk_maturity_rating(connection: Connection, maturity_rating_id: int):
    query: str = """
                    DELETE FROM public.risk_maturity_rating
                    WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                maturity_rating_id,
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting risk maturity rating {e}")

def edit_risk_maturity_rating(connection: Connection, maturity_rating: RiskMaturityRating, maturity_rating_id: int):
    query: str = """
                    UPDATE public.risk_maturity_rating
                    SET
                    name = %s
                    WHERE id = %s 
                  """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                maturity_rating.name,
                maturity_rating_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating risk maturity rating {e}")

def get_company_risk_maturity_rating(connection: Connection, company_id: int):
    query: str = """
                   SELECT * from public.risk_maturity_rating WHERE company = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (company_id,))
            rows = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching company risk maturity rating {e}")

def get_risk_maturity_rating(connection: Connection, maturity_rating_id):
    query: str = """
                   SELECT * from public.risk_maturity_rating WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (maturity_rating_id,))
            rows = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching risk maturity rating {e}")