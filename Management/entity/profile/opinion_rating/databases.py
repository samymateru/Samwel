from fastapi import HTTPException
from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.entity.profile.opinion_rating.schemas import *
from psycopg import AsyncConnection, sql

def new_opinion_rating(connection: Connection, opinion_rating: OpinionRating, company_id: str):
    query: str = """
                    INSERT INTO public.opinion_rating (company, name) VALUES(%s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
               company_id,
                opinion_rating.name
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding opinion rating {e}")

def delete_opinion_rating(connection: Connection, opinion_rating_id: int):
    query: str = """
                    DELETE FROM public.opinion_rating
                    WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
               opinion_rating_id,
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting opinion rating {e}")

def edit_opinion_rating(connection: Connection, opinion_rating: OpinionRating, opinion_rating_id: int):
    query: str = """
                    UPDATE public.opinion_rating
                    SET
                    name = %s
                    WHERE id = %s 
                  """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                opinion_rating.name,
                opinion_rating_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating opinion rating {e}")

async def get_company_opinion_rating(connection: AsyncConnection, company_id: str):
    query = sql.SQL("SELECT * from public.opinion_rating WHERE company = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching company opinion rating {e}")