from fastapi import HTTPException
from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.entity.profile.issue_source.schemas import *
from psycopg import AsyncConnection, sql

def new_issue_source(connection: Connection, issue_source: IssueSource, company_id: str):
    query: str = """
                    INSERT INTO public.issue_source (company, name) VALUES(%s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                company_id,
                issue_source.name
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding issue_source {e}")

def delete_issue_source(connection: Connection, issue_source_id: int):
    query: str = """
                        DELETE FROM public.issue_source
                        WHERE id = %s
                     """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                issue_source_id,
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting issue_source {e}")

def edit_issue_source(connection: Connection, issue_source: IssueSource, issue_source_id: int):
    query: str = """
                    UPDATE public.issue_source
                    SET
                    name = %s
                    WHERE id = %s 
                  """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                issue_source.name,
                issue_source_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating issue_source {e}")

async def get_company_issue_source(connection: AsyncConnection, company_id: str):
    query = sql.SQL("SELECT * from public.issue_source WHERE company = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching company issue_source {e}")
