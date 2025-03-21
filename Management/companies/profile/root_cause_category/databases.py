from collections import defaultdict
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from fastapi import HTTPException
from Management.companies.profile.root_cause_category.schemas import *

def get_combined_root_cause_category(connection: Connection, column: str = None, value: str | int = None):
    query = """
            SELECT 
            public.root_cause_category.name,
            public.root_cause_category.id,
            public.root_cause_sub_category.sub_name
            FROM public.root_cause_category INNER JOIN public.root_cause_sub_category
            ON public.root_cause_category.id = public.root_cause_sub_category.root_cause_category
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
            print(query)
            sub_process_dict = defaultdict(list)

            for item in data:
                key = (item["name"], item["id"])
                sub_process_dict[key].append(item["sub_name"])

            sub_process_list = [
                {"root_cause": name, "id": id, "sub_root_cause": sub_processes}
                for (name, id), sub_processes in sub_process_dict.items()
            ]
            return sub_process_list
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching combined root cause {e}")