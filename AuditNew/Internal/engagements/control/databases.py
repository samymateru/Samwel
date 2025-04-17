from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.control.schemas import *

def add_new_control(connection: Connection, control: Control, sub_program_id: int):
    query: str = """
                    INSERT INTO public.control (sub_program, name, objective, type) VALUES (%s, %s, %s, %s) RETURNING id;
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(
                sub_program_id,
                control.name,
                control.objective,
                control.type
            ))
            connection.commit()
            return cursor.fetchone()[0]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating control {e}")

def edit_control(connection: Connection, control: Control, control_id: int):
    query: str = """
                    UPDATE public.control
                    SET 
                    name = %s,
                    objective = %s,
                    type = %s
                    WHERE id = %s;         
                  """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(
                control.name,
                control.objective,
                control.type,
                control_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating control {e}")

def remove_control(connection: Connection, control_id: int):
    query: str = """
                  DELETE FROM public.control WHERE id = %s;
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(control_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting control {e}")

def get_control(connection: Connection, sub_program_id: int):
    query: str = """
                  SELECT * FROM public.control WHERE sub_program = %s;
                 """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (sub_program_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching controls {e}")
