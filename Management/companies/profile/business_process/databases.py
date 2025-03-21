from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from fastapi import HTTPException
from collections import defaultdict


def get_combined_business_process(connection: Connection, column: str = None, value: str | int = None):
    query = """
            SELECT 
            public.business_process.process_name,
            public.business_process.id,
            public.business_process.code,
            public.business_sub_process.name
            FROM public.business_process INNER JOIN public.business_sub_process
            ON public.business_process.id = public.business_sub_process.business_process
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
                key = (item["process_name"], item["code"], item["id"])
                sub_process_dict[key].append(item["name"])

            sub_process_list = [
                {"process_name": name, "code": code, "id": id, "sub_process_name": sub_processes}
                for (name, code, id), sub_processes in sub_process_dict.items()
            ]
            return sub_process_list
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching business process: {e}")