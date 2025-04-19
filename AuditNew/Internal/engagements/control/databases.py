from fastapi import HTTPException
from AuditNew.Internal.engagements.control.schemas import *
from psycopg import AsyncConnection, sql
from utils import get_unique_key
from psycopg.errors import ForeignKeyViolation, UniqueViolation

async def add_new_control(connection: AsyncConnection, control: Control, sub_program_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.control (id, sub_program, name, objective, type) 
        VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query,(
                get_unique_key(),
                sub_program_id,
                control.name,
                control.objective,
                control.type
            ))
            control_id = await cursor.fetchone()
            await connection.commit()
            return control_id[0]
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Sub program id is invalid")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Control already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating control {e}")

async def edit_control(connection: AsyncConnection, control: Control, control_id: str):
    query = sql.SQL(
        """
        UPDATE public.control
        SET 
        name = %s,
        objective = %s,
        type = %s
        WHERE id = %s;         
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query,(
                control.name,
                control.objective,
                control.type,
                control_id
            ))
        await connection.commit()
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Regulation already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating control {e}")

async def remove_control(connection: AsyncConnection, control_id: str):
    query = sql.SQL("DELETE FROM public.control WHERE id = %s;")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query,(control_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting control {e}")

async def get_control(connection: AsyncConnection, sub_program_id: str):
    query = sql.SQL("SELECT * FROM public.control WHERE sub_program = %s;")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (sub_program_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching controls {e}")
