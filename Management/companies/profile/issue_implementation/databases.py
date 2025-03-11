from fastapi import HTTPException
from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from Management.companies.profile.issue_implementation.schemas import *

def new_issue_implementation(connection: Connection, issue_implementation: IssueImplementation, company_id: int):
    query: str = """
                    INSERT INTO public.issue_implementation (company, name) VALUES(%s, %s)
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
               company_id,
                issue_implementation.name
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding issue_implementation {e}")

def delete_issue_implementation(connection: Connection, issue_implementation_id: int):
    query: str = """
                    DELETE FROM public.issue_implementation
                    WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
               issue_implementation_id,
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting issue_implementation {e}")

def edit_issue_implementation(connection: Connection, issue_implementation: IssueImplementation, issue_implementation_id: int):
    query: str = """
                    UPDATE public.issue_implementation
                    SET
                    name = %s
                    WHERE id = %s 
                  """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                issue_implementation.name,
                issue_implementation_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating issue_implementation {e}")

def get_company_issue_implementation(connection: Connection, company_id: int):
    query: str = """
                   SELECT * from public.issue_implementation WHERE company = %s
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
        raise HTTPException(status_code=400, detail=f"Error fetching company issue implementation {e}")

def get_issue_implementation(connection: Connection, issue_implementation_id):
    query: str = """
                    SELECT * from public.issue_implementation WHERE id = %s
                  """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (issue_implementation_id,))
            rows = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching issue implementation {e}")