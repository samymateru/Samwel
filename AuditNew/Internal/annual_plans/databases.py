from fastapi import HTTPException
from psycopg2.extensions import cursor as Cursor
from psycopg2.extensions import connection as Connection
from typing import List, Tuple, Dict
from AuditNew.Internal.annual_plans.schemas import UpdateAnnualPlan
from datetime import datetime

def create_new_annual_plan(connection: Connection, annual_plan_data: Tuple) -> None:
    query = """
               INSERT INTO public.annual_plan (name, year, company_id, created_by, created_at, updated_at, status,
               description, audit_type, start_date, end_date) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, annual_plan_data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error occur while adding new annual plan {e}")
        raise HTTPException(status_code=400, detail="Error occur while updating annual plan")

def update_annual_plan(connection: Connection, annual_plan_data: UpdateAnnualPlan) -> None:
    query_parts = []
    params = []

    # Check if the plan_name is set
    if annual_plan_data.name is not None:
        query_parts.append("name = %s")
        params.append(annual_plan_data.name)

    # Check if the start date is set
    if annual_plan_data.start_date is not None:
        query_parts.append("start_date = %s")
        params.append(annual_plan_data.start_date)

    # Check if the end date is set
    if annual_plan_data.end_date is not None:
        query_parts.append("end_date = %s")
        params.append(annual_plan_data.end_date)

    # Check if the status is set
    if annual_plan_data.status is not None:
        query_parts.append("status = %s")
        params.append(annual_plan_data.status)

    # Check if the description is set
    if annual_plan_data.description is not None:
        query_parts.append("description = %s")
        params.append(annual_plan_data.description)

    # Check if the year is set
    if annual_plan_data.year is not None:
        query_parts.append("year = %s")
        params.append(annual_plan_data.year)

    # Check if the audit type is set
    if annual_plan_data.audit_type is not None:
        query_parts.append("audit_type = %s")
        params.append(annual_plan_data.audit_type)

    # If no fields to update, raise an error and return
    if not query_parts:
        raise HTTPException(status_code=400, detail="No fields to update")

    query_parts.append("updated_at = %s")
    params.append(datetime.now())

    # Construct the SET part without trailing commas
    set_clause = ", ".join(query_parts)

    # Add the WHERE condition
    where_clause = "WHERE annual_plan_id = %s"
    params.append(annual_plan_data.annual_plan_id)

    # Combine the SET and WHERE parts into the final query
    query = f"UPDATE public.annual_plan SET {set_clause} {where_clause}"

    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, tuple(params))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error occur while updating annual plan {e}")
        raise HTTPException(status_code=400, detail="Error occur while updating annual plan")

def delete_annual_plan(connection: Connection, annual_plan_id: List[int]) -> None:
    query = """
                DELETE FROM public.annual_plans
                WHERE annual_plan_id = ANY(%s)
                RETURNING annual_plan_id;
                """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (annual_plan_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error occur during delete of the annual plan {e}")
        raise HTTPException(status_code=400, detail="Error occur during delete of the annual plan")

def get_annual_plans(connection: Connection,  column: str = None, value: str = None, row: str = None) -> List[Dict]:
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
        print(f"error occur while trying to get annual plans {e}")
        raise HTTPException(status_code=400, detail="Error querying annual plans")
