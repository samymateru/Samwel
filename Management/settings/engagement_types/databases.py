from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from fastapi import HTTPException
from collections import defaultdict

def get_engagement_types(connection: Connection, column: str = None, value: str = None):
    query = f"""
            SELECT * from public.engagement_types
            """
    if column and value:
        query += f"WHERE  {column} = %s"

    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            print(data)
            return data
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement types: {e}")
