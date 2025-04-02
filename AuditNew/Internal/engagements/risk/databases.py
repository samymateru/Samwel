from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.risk.schemas import *

def add_new_risk(connection: Connection, risk: Risk, engagement_id: int):
    query: str = """
                    INSERT INTO public.risk (engagement, name, ref, rating) VALUES (%s, %s, %s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(
                engagement_id,
                risk.name,
                risk.ref,
                risk.rating
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating risk {e}")

def edit_risk(connection: Connection, risk: Risk, risk_id: int):
    query: str = """
                    UPDATE public.issue
                    SET 
                    name = %s,
                    WHERE id = %s;         
                  """

def remove_risk(connection: Connection, risk_id: int):
    pass