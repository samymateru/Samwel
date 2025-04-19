from fastapi import HTTPException
from AuditNew.Internal.engagements.risk.schemas import *
from psycopg import AsyncConnection, sql
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from utils import get_unique_key

async def add_new_risk(connection: AsyncConnection, risk: Risk, sub_program_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.risk (id, sub_program, name, rating) 
        VALUES (%s, %s, %s, %s) RETURNING id;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query,(
                get_unique_key(),
                sub_program_id,
                risk.name,
                risk.rating
            ))
            risk_id = await cursor.fetchone()
            await connection.commit()
            return risk_id[0]
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Sub program id is invalid")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Risk is already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating risk {e}")

async def edit_risk(connection: AsyncConnection, risk: Risk, risk_id: str):
    query = sql.SQL(
        """
        UPDATE public.risk
        SET 
        name = %s,
        rating = %s
        WHERE id = %s;         
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query,(
                risk.name,
                risk.rating,
                risk_id
            ))
        await connection.commit()
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Risk already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating risk {e}")

async def remove_risk(connection: AsyncConnection, risk_id: str):
    query = sql.SQL("DELETE FROM public.risk WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query,(risk_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting risk {e}")


async def get_risk(connection: AsyncConnection, sub_program_id: str):
    query = sql.SQL("SELECT * FROM public.risk WHERE sub_program = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (sub_program_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching risk {e}")
