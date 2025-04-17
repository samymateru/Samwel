from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.risk.schemas import *

def add_new_risk(connection: Connection, risk: Risk, sub_program_id: int):
    query: str = """
                    INSERT INTO public.risk (sub_program, name, rating) VALUES (%s, %s, %s) RETURNING id;
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(
                sub_program_id,
                risk.name,
                risk.rating
            ))
            connection.commit()
            return cursor.fetchone()[0]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating risk {e}")

def edit_risk(connection: Connection, risk: Risk, risk_id: int):
    query: str = """
                    UPDATE public.risk
                    SET 
                    name = %s,
                    rating = %s
                    WHERE id = %s;         
                  """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(
                risk.name,
                risk.rating,
                risk_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating risk {e}")

def remove_risk(connection: Connection, risk_id: int):
    query: str = """
                  DELETE FROM public.risk WHERE id = %s;
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(risk_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting risk {e}")


def get_risk(connection: Connection, sub_program_id: int):
    query: str = """
                  SELECT * FROM public.risk WHERE sub_program = %s;
                 """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (sub_program_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching risk {e}")
