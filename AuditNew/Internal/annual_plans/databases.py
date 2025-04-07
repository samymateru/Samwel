from fastapi import HTTPException
from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from typing import List, Tuple, Dict
from AuditNew.Internal.annual_plans.schemas import *
from datetime import datetime

def add_new_annual_plan(connection: Connection, audit_plan: AnnualPlan, company_module_id: int):
    query = """
                INSERT INTO public.annual_plans (company_module, name, year, status, start, "end", attachment, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                company_module_id,
                audit_plan.name,
                audit_plan.year,
                audit_plan.status,
                audit_plan.start,
                audit_plan.end,
                audit_plan.attachment,
                datetime.now()
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error occur while adding annual plan {e}")

def edit_annual_plan(connection: Connection, annual_plan: AnnualPlan, annual_plan_id: int):
    query: str = """
                   UPDATE public.annual_plan SET 
                   name = %s,
                   year = %s,
                   start = %s,
                   "end" = %s,
                   status = %s,
                   attachment = %s
                   WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                annual_plan.name,
                annual_plan.year,
                annual_plan.start,
                annual_plan.end,
                annual_plan.status,
                annual_plan.attachment,
                annual_plan_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error occur while updating annual plan {e}")

def remove_annual_plan(connection: Connection, annual_plan_id: int):
    query = """
                DELETE FROM public.annual_plans
                WHERE id = %s
                """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (annual_plan_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting annual plan {e}")

def get_annual_plans(connection: Connection,  column: str = None, value: str | int  = None, row: str = None) -> List[Dict]:
    query = "SELECT * FROM public.annual_plans "
    if row:
        query = f"SELECT {row} FROM public.annual_plans "
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
        raise HTTPException(status_code=400, detail=f"Error querying annual plans {e}")
