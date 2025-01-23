from typing import Tuple, List, Dict
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor

from Management.templates.schemas import NewTemplate

def create_engagement_template(connection: Connection, template: NewTemplate, company_id: str):
    query_ = """
            INSERT INTO public.templates (name, category, company_id, created_at) VALUES (%s, %s, %s,%s) RETURNING id;
            """
    query = """
            INSERT INTO public.engagement_template (phases,actions, procedures, template_id) VALUES (%s, %s, %s, %s)
            """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query_, (
                template.name,
                template.category,
                company_id,
                template.created_at
            ))
            template_id = cursor.fetchall()[0][0]
            cursor.execute(query, (
                template.phases,
                template.actions,
                template.procedures,
                template_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error creating engagement template {e}")
        raise HTTPException(status_code=400, detail="Error creating template")

def get_template(connection: Connection, company_id: str, column: str = None, value: str = None, row: str = None):
    query = """
            SELECT 
            t.id AS template_id,
            t.name AS template_name,
            t.category,
            t.company_id,
            t.created_at,
            e.phases,
            e.actions,
            e.procedures
            FROM 
            public.templates t
            INNER JOIN 
            public.engagement_template e
            ON 
            t.id = e.template_id
            WHERE 
            t.company_id = %s;
            """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (company_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        print(f"Error querying templates {e}")
        raise HTTPException(status_code=400, detail="Error querying templates")


