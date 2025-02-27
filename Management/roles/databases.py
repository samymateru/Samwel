import json
from typing import Tuple, List, Dict
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from Management.roles.schemas import *


def get_roles(connection: Connection, column: str = None, value: str = None):
    query = "SELECT * FROM public.roles "
    if column and value:
        query += f"WHERE  {column} = %s"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying roles {e}")

def add_role(connection: Connection, data: NewRole, company_id: int):
    query = "INSERT INTO public.roles (company, roles) VALUES(%s, %s)"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (company_id, data.model_dump_json()))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error deleting engagement {e}")
        raise HTTPException(status_code=400, detail="Error deleting engagement")


