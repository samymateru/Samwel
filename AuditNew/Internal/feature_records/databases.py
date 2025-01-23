from typing import Tuple
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from typing import List,Dict
from AuditNew.Internal.feature_records.schemas import UpdateFeatureRecord
from fastapi import HTTPException
from datetime import datetime

def create_new_feature_record(connection: Connection, feature_record_data: Tuple) -> None:
    query = """
               INSERT INTO public.feature_records (feature_id, title, record_type, data, created_by, updated_by
               created_at, updated_at) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
               """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, feature_record_data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error creating new feature record {e}")
        raise HTTPException(status_code=400, detail="Error creating new feature record")

def update_feature_record(connection: Connection, feature_record_data: UpdateFeatureRecord) -> None:
    query_parts = []
    params = []

    # Check if the feature id is set
    if feature_record_data.feature_id is not None:
        query_parts.append("feature_id = %s")
        params.append(feature_record_data.feature_id)

    # Check if the title is set
    if feature_record_data.title is not None:
        query_parts.append("title = %s")
        params.append(feature_record_data.title)

    # Check if the record type is set
    if feature_record_data.record_type is not None:
        query_parts.append("record_type = %s")
        params.append(feature_record_data.record_type)

    # Check if the  data is set
    if feature_record_data.data is not None:
        query_parts.append("data = %s")
        params.append(feature_record_data.data)

    # If no fields to update, raise an error and return
    if not query_parts:
        raise HTTPException(status_code=400, detail="No fields to update")

    query_parts.append("updated_at = %s")
    params.append(datetime.now())

    set_clause = ", ".join(query_parts)
    # Add the WHERE condition
    where_clause = "WHERE record_id = %s"
    params.append(feature_record_data.record_id)

    # Combine the SET and WHERE parts into the final query
    query = f"UPDATE public.feature_records SET {set_clause} {where_clause}"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, tuple(params))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error updating feature record {e}")
        raise HTTPException(status_code=400, detail="Error updating feature record")

def delete_feature_record(connection: Connection, feature_record_id: List[int]) -> None:
    query = """
               DELETE FROM public.feature_records
               WHERE record_id = ANY(%s)
               RETURNING record_id;
               """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (feature_record_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error deleting feature record {e}")
        raise HTTPException(status_code=400, detail="Error deleting feature record")

def get_feature_records(connection: Connection, column: str = None, value: str = None, row: str = None) -> List[Dict]:
    query = "SELECT * FROM public.feature_records "
    if row:
        query = f"SELECT {row} FROM public.feature_records "
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
        print(f"Error querying feature records {e}")
        raise HTTPException(status_code=400, detail="Error querying feature records")