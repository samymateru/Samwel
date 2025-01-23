from typing import Tuple
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from typing import List,Dict
from AuditNew.Internal.planning_details.schemas import UpdatePlanningDetails
from fastapi import HTTPException
from datetime import datetime

def create_new_planning_detail(connection: Connection, planning_detail_data: Tuple) -> None:
    query = """
               INSERT INTO public.planning_details (engagement_id, task, notes, status, created_by, created_at,) 
               VALUES (%s, %s, %s, %s, %s, %s)
               """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, planning_detail_data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error creating planning detail {e}")
        raise HTTPException(status_code=400, detail="Error creating planning detail")

def update_planning_detail(connection: Connection, planning_detail_data: UpdatePlanningDetails) -> None:
    query_parts = []
    params = []

    # Check if the engagement id is set
    if planning_detail_data.engagement_id is not None:
        query_parts.append("engagement_id = %s")
        params.append(planning_detail_data.engagement_id)

    # Check if the task is set
    if planning_detail_data.task is not None:
        query_parts.append("task = %s")
        params.append(planning_detail_data.task)

    # Check if the notes is set
    if planning_detail_data.notes is not None:
        query_parts.append("notes = %s")
        params.append(planning_detail_data.notes)

    # Check if the status is set
    if planning_detail_data.status is not None:
        query_parts.append("status = %s")
        params.append(planning_detail_data.status)

    # If no fields to update, raise an error and return
    if not query_parts:
        raise HTTPException(status_code=400, detail="No fields to update")

    query_parts.append("updated_at = %s")
    params.append(datetime.now())

    set_clause = ", ".join(query_parts)
    # Add the WHERE condition
    where_clause = "WHERE planning_id = %s"
    params.append(planning_detail_data.planning_id)

    # Combine the SET and WHERE parts into the final query
    query = f"UPDATE public.planning_details SET {set_clause} {where_clause}"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, tuple(params))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error updating planning detail {e}")
        raise HTTPException(status_code=400, detail="Error updating planning detail")

def delete_planning_details(connection: Connection, planning_id: List[int]) -> None:
    query = """
               DELETE FROM public.planning_details
               WHERE planning_id = ANY(%s)
               RETURNING planning_id;
               """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (planning_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error deleting planning details {e}")
        raise HTTPException(status_code=400, detail="Error deleting planning details")

def get_planning_details(connection: Connection, column: str = None, value: str = None, row: str = None) -> List[Dict]:
    query = "SELECT * FROM public.planning_details "
    if row:
        query = f"SELECT {row} FROM public.planning_details "
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
        print(f"Error querying planning details {e}")
        raise HTTPException(status_code=400, detail="Error querying planning details")