from fastapi import HTTPException
from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.entity.profile.engagement_type.schemas import *
from psycopg import AsyncConnection, sql

def new_engagement_type(connection: Connection, engagement_type: EngagementType, company_id: str):
    query: str = """
                    INSERT INTO public.engagement_types (company, name) VALUES(%s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
               company_id,
                engagement_type.name
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement type {e}")

def delete_engagement_type(connection: Connection, engagement_type_id: int):
    query: str = """
                    DELETE FROM public.engagement_types
                    WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
               engagement_type_id,
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting engagement type {e}")

def edit_engagement_type(connection: Connection, engagement_type: EngagementType, engagement_type_id: int):
    query: str = """
                    UPDATE public.engagement_types
                    SET
                    name = %s
                    WHERE id = %s 
                  """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                engagement_type.name,
                engagement_type_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating engagement type {e}")

async def get_company_engagement_type(connection: AsyncConnection, company_id: str):
    query = sql.SQL("SELECT * from public.engagement_types WHERE company = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching company engagement type {e}")