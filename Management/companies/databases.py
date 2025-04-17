from typing import Dict
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from psycopg2.extras import RealDictCursor
from Management.companies.schemas import *
from fastapi import HTTPException
from datetime import datetime
from psycopg import AsyncConnection
from psycopg import sql

def create_new_company(connection: Connection, company_data: NewCompany):
    query_insert = """
        INSERT INTO public.companies (name, owner, email, telephone, website, entity_type, status, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
    """
    query_check = "SELECT 1 FROM public.companies WHERE email = %s"
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            # Check if the company already exists
            cursor.execute(query_check, (company_data.email,))
            if cursor.fetchone():
               raise HTTPException(status_code=409, detail="Company already exists")

            # Insert new company and return the ID
            cursor.execute(query_insert, (
                company_data.name,
                company_data.owner,
                company_data.email,
                company_data.telephone,
                company_data.website,
                company_data.entity_type,
                company_data.status,
                datetime.now()
            ))
            connection.commit()
            return cursor.fetchone()["id"]
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating new company {e}")

def get_companies(connection: Connection, company_id: int) -> List[Dict]:
    query = """SELECT * FROM public.companies WHERE id = %s"""


    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (company_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        connection.rollback()
        print(f"Error querying companies {e}")
        raise HTTPException(status_code=400, detail="Error querying companies")


async def get_companies_async(connection: AsyncConnection, company_id: int):
    query = sql.SQL("""SELECT * FROM public.companies WHERE id = %s""")

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Error querying companies")



