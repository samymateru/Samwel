import json
from typing import Tuple, List, Dict
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from Management.roles.schemas import *


def get_roles(connection: Connection, column: str = None, value: str | int = None):
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

def add_role(connection: Connection, role: Category, company_id: int):
    query:str = """
                  UPDATE public.roles
                  SET roles = roles || %s::jsonb
                  WHERE company = %s;
                """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (role.model_dump_json(), company_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating roles {e}")

def edit_role(connection: Connection, role: Category, company_id: int, name: str):
    query: str = """
                   UPDATE roles
                   SET roles = %s::jsonb
                   WHERE company = %s;
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute("SELECT roles FROM roles WHERE company = %s;", (company_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=203, detail="No roles")
            roles = result[0]
            for role_ in roles:
                if role_["name"] == name:
                    role_["name"] = role.name  # Update the role name
                    role_["permissions"] = role.permissions.model_dump()  # Update permissions
                    break
            cursor.execute(query, (json.dumps(roles), company_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating roles {e}")


