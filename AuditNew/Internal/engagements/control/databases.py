from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.control.schemas import *

def add_new_control(connection: Connection, control: Control, sub_program_id: int):
    query: str = """
                    INSERT INTO public.control (sub_program, name, objective, type) VALUES (%s, %s, %s, %s)
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
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating control {e}")

def edit_control(connection: Connection, control: Control, control_id: int):
    pass

def remove_control(connection: Connection, control_id: int):
    pass