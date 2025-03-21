from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from fastapi import HTTPException

def get_root_cause_category(connection: Connection, company_id: int):
    query: str = """
                    SELECT * FROM
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (company_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching business process: {e}")