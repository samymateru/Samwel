from typing import Tuple, List, Dict
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from psycopg2.extras import RealDictCursor
from datetime import datetime
from Management.companies.schemas import UpdateCompany, NewCompany
from fastapi import HTTPException
from datetime import datetime

def create_new_company(connection: Connection, company_data: NewCompany) -> int:
    query_insert = """
        INSERT INTO public.companies (name, owner, email, telephone, website, description, status, created_at) 
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
                company_data.description,
                company_data.status,
                datetime.now()
            ))
            connection.commit()
            return cursor.fetchone()["id"]
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        print(f"Error creating new company: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating new company")


def update_company(connection: Connection, company_data: UpdateCompany):
    query_parts = []
    params = []

    # Check if the name is set
    if company_data.name is not None:
        query_parts.append("name = %s")
        params.append(company_data.name)

    # Check if the description data is set
    if company_data.description is not None:
        query_parts.append("description = %s")
        params.append(company_data.description)

    # Check if the owner data is set
    if company_data.owner is not None:
        query_parts.append("owner = %s")
        params.append(company_data.owner)

    # Check if the email date is set
    if company_data.email is not None:
        query_parts.append("email = %s")
        params.append(company_data.email)

    # Check if the  telephone is set
    if company_data.telephone is not None:
        query_parts.append("telephone = %s")
        params.append(company_data.telephone)

    # Check if the  status is set
    if company_data.status is not None:
        query_parts.append("status = %s")
        params.append(company_data.status)

    # Check if the  website is set
    if company_data.website is not None:
        query_parts.append("website = %s")
        params.append(company_data.website)


        # If no fields to update, raise an error and return
    if not query_parts:
        raise HTTPException(status_code=300, detail="No fields to update")

    query_parts.append("updated_at = %s")
    params.append(datetime.now())

    # Construct the SET part without trailing commas
    set_clause = ", ".join(query_parts)

    # Add the WHERE condition
    where_clause = "WHERE id = %s"
    params.append(company_data.company_id)

    # Combine the SET and WHERE parts into the final query
    query = f"UPDATE public.company SET {set_clause} {where_clause}"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, tuple(params))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error updating company {e}")
        raise HTTPException(status_code=400, detail="Error updating company")

def delete_company(connection: Connection, company_id: List[int]):
    query = """
            DELETE FROM public.companies
            WHERE id = ANY(%s)
            RETURNING id;
            """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, str(company_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error deleting module {e}")
        raise HTTPException(status_code=400, detail="Error deleting module")

def get_companies(connection: Connection, column: str = None, value: str = None, row: str = None) -> List[Dict]:
    query = "SELECT * FROM public.companies "
    if row:
        query = f"SELECT {row} FROM public.companies "
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
        print(f"Error querying companies {e}")
        raise HTTPException(status_code=400, detail="Error querying companies")