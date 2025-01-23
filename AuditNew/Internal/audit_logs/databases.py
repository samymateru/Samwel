from typing import Tuple, List, Dict
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.audit_logs.schemas import UpdateAuditLog
from fastapi import  HTTPException
from datetime import datetime

def create_new_audit_log(connection: Connection, audit_log_data: Tuple) -> None:
    query = """
               INSERT INTO public.audit_log (user_id, action, description, created_at, updated_at) 
               VALUES (%s, %s, %s, %s, %s)
               """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, audit_log_data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error creating audit log {e}")
        raise HTTPException(status_code=400, detail="Error creating audit log")

def update_audit_log(connection: Connection, audit_log_data: UpdateAuditLog) -> None:
    query_parts = []
    params = []

    # Check if the action is set
    if audit_log_data.action is not None:
        query_parts.append("action = %s")
        params.append(audit_log_data.action)

    # Check if the description is set
    if audit_log_data.description is not None:
        query_parts.append("description = %s")
        params.append(audit_log_data.description)


    # If no fields to update, raise an error and return
    if not query_parts:
        raise HTTPException(status_code=400, detail="No fields to update")

    query_parts.append("updated_at = %s")
    params.append(datetime.now())

    # Construct the SET part without trailing commas
    set_clause = ", ".join(query_parts)

    # Add the WHERE condition
    where_clause = "WHERE log_id = %s"
    params.append(audit_log_data.log_id)

    # Combine the SET and WHERE parts into the final query
    query = f"UPDATE public.audit_log SET {set_clause} {where_clause}"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, tuple(params))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error updating audit log {e}")
        raise HTTPException(status_code=400, detail="Error updating audit log")

def delete_audit_log(connection: Connection, log_id: List[int]) -> None:
    query = """
            DELETE FROM public.audit_log
            WHERE log_id = ANY(%s)
            RETURNING log_id;
            """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (log_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error update audit log {e}")
        raise HTTPException(status_code=400, detail="Error delete audit log")

def get_audit_logs(connection: Connection, column: str = None, value: str = None, row: str = None) -> List[Dict]:
    query = "SELECT * FROM public.audit_log "
    if row:
        query = f"SELECT {row} FROM public.audit_log "
    if column and value:
        query += f"WHERE  {column} = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        print(f"Error querying audit plans {e}")
        raise HTTPException(status_code=400, detail="Error querying audit plans")