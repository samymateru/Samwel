from typing import Tuple
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from typing import List, Dict
from AuditNew.Internal.staff_assignment.schemas import UpdateStaffAssignment
from fastapi import HTTPException

def create_new_staff_assignment(connection: Connection, staff_assignment_data: Tuple) -> None:
    query = """
               INSERT INTO public.engagement_staff_assign (engagement_id, user_id, role) 
               VALUES (%s, %s, %s)
               """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, staff_assignment_data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error creating engagement assignment {e}")
        raise HTTPException(status_code=400, detail="Error creating engagement assignment")

def update_staff_assignment(connection: Connection, staff_assignment_data: UpdateStaffAssignment) -> None:
    query_parts = []
    params = []

    # Check if the engagement id is set
    if staff_assignment_data.engagement_id is not None:
        query_parts.append("engagement_id = %s")
        params.append(staff_assignment_data.engagement_id)

    # Check if the user id is set
    if staff_assignment_data.user_id is not None:
        query_parts.append("user_id = %s")
        params.append(staff_assignment_data.user_id)

    # Check if the role is set
    if staff_assignment_data.role is not None:
        query_parts.append("role = %s")
        params.append(staff_assignment_data.role)

    # If no fields to update, raise an error and return
    if not query_parts:
        raise HTTPException(status_code=400, detail="No fields to update")

    set_clause = ", ".join(query_parts)
    # Add the WHERE condition
    where_clause = "WHERE assignment_id = %s"
    params.append(staff_assignment_data.assignment_id)

    # Combine the SET and WHERE parts into the final query
    query = f"UPDATE public.engagement_staff_assign SET {set_clause} {where_clause}"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, tuple(params))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error updating engagement staff assignment {e}")
        raise HTTPException(status_code=400, detail="Error updating engagement staff assignment")

def delete_staff_assignment(connection: Connection, staff_assignment_id: List[int]) -> None:
    query = """
               DELETE FROM public.engagement_staff_assign
               WHERE assignment_id = ANY(%s)
               RETURNING assignment_id;
               """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (staff_assignment_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error deleting staff assignment {e}")
        raise HTTPException(status_code=400, detail="Error deleting staff assignment")

def get_staff_assignment(connection: Connection, column: str = None, value: str = None, row: str = None) -> List[Dict]:
    query = "SELECT * FROM public.engagement_staff_assign "
    if row:
        query = f"SELECT {row} FROM public.engagement_staff_assign "
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
        print(f"Error querying engagement staff assignment {e}")
        raise HTTPException(status_code=400, detail="Error querying engagement staff assignment")