from collections import defaultdict

from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor

def get_combined_risk_category(connection: Connection, column: str = None, value: str | int = None):
    query = """
            SELECT 
            public.risk_category.name,
            public.risk_category.id,
            public.sub_risk_category.sub_name
            FROM public.risk_category INNER JOIN public.sub_risk_category
            ON public.risk_category.id = public.sub_risk_category.risk_category
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
            sub_process_dict = defaultdict(list)

            for item in data:
                key = (item["name"], item["id"])
                sub_process_dict[key].append(item["sub_name"])

            sub_process_list = [
                {"risk_category": name, "id": id, "sub_risk_category": sub_processes}
                for (name, id), sub_processes in sub_process_dict.items()
            ]
            return sub_process_list
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching risk categories {e}")