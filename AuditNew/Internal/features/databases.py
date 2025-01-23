from typing import Tuple, List, Dict
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.features.schemas import UpdateFeature
from datetime import datetime

def create_new_feature(connection: Connection, feature_data: Tuple):
    query = """
                INSERT INTO public.feature (module_id, name, description, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, feature_data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error creating feature {e}")
        raise HTTPException(status_code=400, detail="Error creating feature")

def update_feature(connection: Connection, feature_data: UpdateFeature):
    query_parts = []
    params = []

    #Check if the name is set
    if feature_data.name is not None:
        query_parts.append("name = %s")
        params.append(feature_data.name)

    #Check if the description is set
    if feature_data.description is not None:
        query_parts.append("description = %s")
        params.append(feature_data.description)

    # Check if the module id is set
    if feature_data.module_id is not None:
        query_parts.append("module_id = %s")
        params.append(feature_data.module_id)

    # Check if is active is set
    if feature_data.is_active is not None:
        query_parts.append("is_active = %s")
        params.append(feature_data.is_active)

    # If no fields to update, raise an error and return
    if not query_parts:
        raise HTTPException(status_code=400, detail="No fields to update")

    query_parts.append("updated_at = %s")
    params.append(datetime.now())

    # Construct the SET part without trailing commas
    set_clause = ", ".join(query_parts)

    # Add the WHERE condition
    where_clause = "WHERE feature_id = %s"
    params.append(feature_data.feature_id)

    # Combine the SET and WHERE parts into the final query
    query = f"UPDATE public.feature SET {set_clause} {where_clause}"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, tuple(params))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error updating feature {e}")
        raise HTTPException(status_code=400, detail="Error updating feature")

def delete_features(connection: Connection, feature_id: List[int]):
    query = """
            DELETE FROM public.feature
            WHERE feature_id = ANY(%s)
            RETURNING feature_id;
            """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (feature_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error deleting feature {e}")
        raise HTTPException(status_code=400, detail="Error deleting feature")

def get_features(connection: Connection, column: str = None, value: str = None, row: str = None) -> List[Dict]:
    query = "SELECT * FROM public.feature "
    if row:
        query = f"SELECT {row} FROM public.feature "
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
        print(f"Error querying features {e}")
        raise HTTPException(status_code=400, detail="Error querying features")