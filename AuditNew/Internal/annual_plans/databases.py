from fastapi import HTTPException
from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from typing import Dict
from AuditNew.Internal.annual_plans.schemas import *
from datetime import datetime
from psycopg import AsyncConnection
from psycopg import sql
from psycopg.errors import ForeignKeyViolation, UniqueViolation
import uuid


async def add_new_annual_plan(connection: AsyncConnection, audit_plan: AnnualPlan, company_module_id: int):
    query = sql.SQL(
        """
        INSERT INTO public.annual_plans (id, company_module, name, year, status, start, "end", attachment, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                audit_plan.id,
                company_module_id,
                audit_plan.name,
                audit_plan.year,
                audit_plan.status,
                audit_plan.start,
                audit_plan.end,
                audit_plan.attachment,
                datetime.now()
            ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Invalid company module id")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Annual plan name already exist")

    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error occur while adding annual plan {e}")

def edit_annual_plan(connection: Connection, annual_plan: AnnualPlan, annual_plan_id: int):
    query: str = """
                   UPDATE public.annual_plans SET 
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

async def get_annual_plans(connection: AsyncConnection,  company_module_id: int):
    query = sql.SQL("SELECT * FROM public.annual_plans WHERE company_module = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_module_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying annual plans {e}")




## older implementation
def add_new_annual_plan_(connection: Connection, audit_plan: AnnualPlan, company_module_id: int):
    query = """
                INSERT INTO public.annual_plans (id, company_module, name, year, status, start, "end", attachment, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    try:
        with connection.cursor() as cursor:
            print(audit_plan.id)
            cursor.execute(query, (
                audit_plan.id,
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

def get_annual_plans_(connection: Connection,  company_module_id: int) -> List[Dict]:
    query = "SELECT * FROM public.annual_plans WHERE company_module = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (company_module_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying annual plans {e}")
