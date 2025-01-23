from typing import Tuple
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from typing import List,Dict
from AuditNew.Internal.engagement_profile.schemas import UpdateEngagementProfile
from fastapi import HTTPException

def create_new_engagement_profile(connection: Connection, engagement_profile_data: Tuple) -> None:
    query = """
               INSERT INTO public.engagement_profile (engagement_id, profile_name, key_contacts, estimated_time,
               business_context) 
               VALUES (%s, %s, %s, %s, %s)
               """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, engagement_profile_data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error while creating new engagement profile {e}")
        raise HTTPException(status_code=400, detail="Error while creating new engagement profile")

def update_engagement_profile(connection: Connection, engagement_profile_data: UpdateEngagementProfile) -> None:
    query_parts = []
    params = []

    # Check if the profile name is set
    if engagement_profile_data.profile_name is not None:
        query_parts.append("profile_name = %s")
        params.append(engagement_profile_data.profile_name)

    # Check if the key contacts is set
    if engagement_profile_data.key_contacts is not None:
        query_parts.append("key_contacts = %s")
        params.append(engagement_profile_data.key_contacts)

    # Check if the estimated is set
    if engagement_profile_data.estimated_time is not None:
        query_parts.append("estimated_time = %s")
        params.append(engagement_profile_data.estimated_time)

    # Check if the  business context is set
    if engagement_profile_data.business_context is not None:
        query_parts.append("business_context = %s")
        params.append(engagement_profile_data.business_context)

    # If no fields to update, raise an error and return
    if not query_parts:
        raise HTTPException(status_code=400, detail="No fields to update")


    set_clause = ", ".join(query_parts)
    # Add the WHERE condition
    where_clause = "WHERE profile_id = %s"
    params.append(engagement_profile_data.profile_id)

    # Combine the SET and WHERE parts into the final query
    query = f"UPDATE public.engagement_profile SET {set_clause} {where_clause}"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, tuple(params))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error occur while update engagement profile {e}")
        raise HTTPException(status_code=400, detail="Error occur while update engagement profile")

def delete_engagement_profile(connection: Connection, profile_id: List[int]) -> None:
    query = """
               DELETE FROM public.engagement_profile
               WHERE profile_id = ANY(%s)
               RETURNING profile_id;
               """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (profile_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error occur when deleting engagement profile {e}")
        raise HTTPException(status_code=400, detail="Error occur when deleting engagement profile")

def get_engagement_profile(connection: Connection, column: str = None, value: str = None, row: str = None) -> List[Dict]:
    query = "SELECT * FROM public.engagement_profile "
    if row:
        query = f"SELECT {row} FROM public.engagement_profile "
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
        print(f"Error querying engagement profile {e}")
        raise HTTPException(status_code=400, detail="Error querying engagement profile")