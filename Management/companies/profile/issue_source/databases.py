from fastapi import HTTPException
from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.companies.profile.issue_source.schemas import *

def new_issue_source(connection: Connection, issue_source: IssueSource, company_id: int):
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

def get_company_issue_source(connection: Connection, company_id: int):
    query: str = """
                   SELECT * from public.issue_source WHERE company = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (company_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching company issue_source {e}")

def get_issue_source(connection: Connection, issue_source_id):
    query: str = """
                   SELECT * from public.issue_source WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (issue_source_id,))
            rows = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching issue source {e}")