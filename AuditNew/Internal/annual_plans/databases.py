from fastapi import HTTPException
from AuditNew.Internal.annual_plans.schemas import *
from datetime import datetime
from psycopg import AsyncConnection, sql
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from utils import check_row_exists, get_unique_key


async def add_new_annual_plan(connection: AsyncConnection, audit_plan: AnnualPlan, company_module_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.annual_plans (id, reference, module, name, year, status, start, "end", attachment, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """)

    get_plan_count = sql.SQL(
        """
        SELECT plan_reference FROM modules WHERE id = {company_module_id}
        """).format(company_module_id=sql.Literal(company_module_id))

    update_module = sql.SQL(
        """
        UPDATE public.modules
        SET plan_reference = %s
        WHERE id = %s
        """)
    try:
        async with connection.cursor() as cursor:
            exists = await check_row_exists(connection=connection, table_name="annual_plans", filters={
                "name": audit_plan.name,
                "module": company_module_id
            })
            if exists:
                raise HTTPException(status_code=400, detail="Audit plan already exists")
            await cursor.execute(get_plan_count)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            module_data = [dict(zip(column_names, row_)) for row_ in rows]
            reference = module_data[0].get("plan_reference") + 1
            await cursor.execute(query, (
                get_unique_key(),
                "P-{:05d}".format(reference),
                company_module_id,
                audit_plan.name,
                audit_plan.year,
                audit_plan.status,
                audit_plan.start,
                audit_plan.end,
                audit_plan.attachment,
                datetime.now()
            ))
            await cursor.execute(update_module, (reference, company_module_id))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Invalid company module id")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Annual plan name already exist")
    except HTTPException:
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error occur while adding annual plan {e}")

async def edit_annual_plan(connection: AsyncConnection, annual_plan: AnnualPlan, annual_plan_id: str):
    query = sql.SQL(
        """
           UPDATE public.annual_plans SET 
           name = %s,
           year = %s,
           start = %s,
           "end" = %s,
           status = %s,
           attachment = %s
           WHERE id = %s
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                annual_plan.name,
                annual_plan.year,
                annual_plan.start,
                annual_plan.end,
                annual_plan.status,
                annual_plan.attachment,
                annual_plan_id
            ))
        await connection.commit()
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Annual plan already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error occur while updating annual plan {e}")

async def remove_annual_plan(connection: AsyncConnection, annual_plan_id: str):
    query = sql.SQL("DELETE FROM public.annual_plans WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (annual_plan_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting annual plan {e}")

async def get_annual_plans(connection: AsyncConnection,  company_module_id: str):
    query = sql.SQL("SELECT * FROM public.annual_plans WHERE module = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_module_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying annual plans {e}")


async def get_annual_plan(connection: AsyncConnection,  plan_id: str):
    query = sql.SQL("SELECT * FROM public.annual_plans WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (plan_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying annual plan data {e}")