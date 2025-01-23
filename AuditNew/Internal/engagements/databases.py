from typing import Dict, List, Tuple
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.schemas import UpdateEngagement, NewEngagement

def create_new_engagement(connection: Connection, engagement_data: NewEngagement, annual_plan_id: str):
    query = """
                INSERT INTO public.engagement (annual_plan_id, engagement_name, engagement_risk,
                 engagement_type, template_id, engagement_status, engagement_phase, quarter, start_date, end_date,
                 created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    try:
        with connection.cursor() as cursor:
            print(str(engagement_data.engagement_phase))
            cursor: Cursor
            cursor.execute(query,
                           (
                               annual_plan_id,
                               engagement_data.engagement_name,
                               engagement_data.engagement_risk,
                               engagement_data.engagement_type,
                               engagement_data.template_id,
                               engagement_data.engagement_status,
                               engagement_data.engagement_phase,
                               engagement_data.quarter,
                               engagement_data.start_date,
                               engagement_data.end_date,
                               engagement_data.created_at
                           ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error creating engagement {e}")
        raise HTTPException(status_code=400, detail="Error creating engagement")

def update_engagement(connection: Connection, engagement_data: UpdateEngagement):
    query_parts = []
    params = []

    # Check if the engagement_name is set
    if engagement_data.engagement_name is not None:
        query_parts.append("engagement_name = %s")
        params.append(engagement_data.engagement_name)

    # Check if the engagement risk is set
    if engagement_data.engagement_risk is not None:
        query_parts.append("engagement_risk = %s")
        params.append(engagement_data.engagement_risk)

    # Check if the engagement type is set
    if engagement_data.engagement_type is not None:
        query_parts.append("engagement_type = %s")
        params.append(engagement_data.engagement_type)

    # Check if the engagement lead is set
    if engagement_data.engagement_lead is not None:
        query_parts.append("engagement_lead = %s")
        params.append(engagement_data.engagement_lead)

    # Check if the engagement status is set
    if engagement_data.engagement_status is not None:
        query_parts.append("engagement_status = %s")
        params.append(engagement_data.engagement_status)

    # Check if the engagement phase is set
    if engagement_data.engagement_phase is not None:
        query_parts.append("engagement_phase = %s")
        params.append(engagement_data.engagement_phase)

    # Check if the quarter is set
    if engagement_data.quarter is not None:
        query_parts.append("quarter = %s")
        params.append(engagement_data.quarter)

    #Check if the start date is set
    if engagement_data.start_date is not None:
        query_parts.append("start_date = %s")
        params.append(engagement_data.start_date)

    # Check if the end date is set
    if engagement_data.end_date is not None:
        query_parts.append("end_date = %s")
        params.append(engagement_data.end_date)

    # If no fields to update, raise an error and return
    if not query_parts:
        raise HTTPException(status_code=400, detail="No fields to update")

    query_parts.append("updated_at = %s")
    params.append(engagement_data.updated_at)

    # Construct the SET part without trailing commas
    set_clause = ", ".join(query_parts)

    # Add the WHERE condition
    where_clause = "WHERE engagement_id = %s"
    params.append(engagement_data.engagement_id)

    # Combine the SET and WHERE parts into the final query
    query = f"UPDATE public.engagement SET {set_clause} {where_clause}"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, tuple(params))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error updating engagement {e}")
        raise HTTPException(status_code=400, detail="Error updating engagement")

def delete_engagements(connection: Connection, engagement_id: List[int]):
    query = """
            DELETE FROM public.engagement
            WHERE engagement_id = ANY(%s)
            RETURNING engagement_id;
            """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (engagement_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error deleting engagement {e}")
        raise HTTPException(status_code=400, detail="Error deleting engagement")


def get_engagements(connection: Connection, column: str = None, value: str = None, row: List[str] = None ) -> List[Dict]:
    query = "SELECT * FROM public.engagement "
    if row:
        query = f"SELECT {" ,".join(row)} FROM public.engagement "
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
        print(f"Error querying engagements {e}")
        raise HTTPException(status_code=400, detail="Error querying engagements")