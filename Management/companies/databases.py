import json
from typing import Tuple, List, Dict
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from psycopg2.extras import RealDictCursor
from datetime import datetime
from Management.companies.schemas import *
from fastapi import HTTPException
from datetime import datetime
from Management.modules import  databases as module_databases
from collections import defaultdict
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
        raise HTTPException(status_code=400, detail="Error deleting module")

def get_companies(connection: Connection, column: str = None, value: str | int = None, row: str = None) -> List[Dict]:
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
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        connection.rollback()
        print(f"Error querying companies {e}")
        raise HTTPException(status_code=400, detail="Error querying companies")

def get_resource(connection: Connection, resource: str, column: str = None, value: str = None, row: str = None) -> List[Dict]:
    query = f"SELECT * FROM public.{resource} "
    if row:
        query = f"SELECT {row} FROM public.{resource} "
    if column and value:
        query += f"WHERE  {column} = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        connection.rollback()
        print(f"Error querying  {resource} {e}")
        raise HTTPException(status_code=400, detail=f"Error querying {resource}")

def get_sub_resource(connection: Connection, resource: str, column: str = None, value: str = None, row: str = None) -> List[Dict]:
    query = f"SELECT * FROM public.{resource} "
    if row:
        query = f"SELECT {row} FROM public.{resource} "
    if column and value:
        query += f"WHERE  {column}_ = %s"
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            return data
    except Exception as e:
        connection.rollback()
        print(f"Error querying  {resource} {e}")
        raise HTTPException(status_code=400, detail=f"Error querying {resource}")



def get_business_process(connection: Connection, column: str = None, value: str = None) -> List[Dict]:
    query = """
            SELECT * FROM public.business_process INNER JOIN public.business_sub_process
            ON public.business_process.id = public.business_sub_process.business_sub_process_
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
            # Extract unique process names with codes
            process_set = {(item["process_name"], item["code"]) for item in data}

            # Step 2: Group sub-processes under their respective process
            sub_process_dict = defaultdict(list)

            for item in data:
                key = (item["process_name"], item["code"])
                sub_process_dict[key].append(item["name"])

            # Convert sub-process dictionary to a list of dictionaries
            sub_process_list = [
                {"process_name": name, "code": code, "sub_process_name": sub_processes}
                for (name, code), sub_processes in sub_process_dict.items()
            ]

            return sub_process_list
    except Exception as e:
        connection.rollback()
        print(f"Error business process {e}")
        raise HTTPException(status_code=400, detail=f"Error business process ")

#################################################################
def add_business_process(connection: Connection, business_process: BusinessProcess, company_id: str):
    query: str = f"INSERT INTO public.business_process (name, code, company) VALUES(%s, %s, %s)"
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (
                business_process.name,business_process.code,
                company_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error creating business process {e}")
        raise HTTPException(status_code=400, detail="Error creating business process")

def add_business_sub_process(connection: Connection, business_sub_process: BusinessSubProcess, business_process_id: str):
    query: str = f"INSERT INTO public.business_sub_process (name, business_process) VALUES(%s, %s)"
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (
                business_sub_process.name,
                business_process_id
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error creating business sub process {e}")
        raise HTTPException(status_code=400, detail="Error creating business sub process")