from typing import Dict
from fastapi import HTTPException
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from Management.company_modules.schemas import *
from psycopg import AsyncConnection, sql
from utils import get_unique_key

async def add_new_company_module(connection: AsyncConnection, company_module: CompanyModule, company_id: int):
    query = sql.SQL(
        """
        INSERT INTO public.company_modules (id, company, name, purchase_date, status)
        VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query,(
                get_unique_key(),
                company_id,
                company_module.name,
                company_module.purchase_date,
                company_module.status
            ))
            module_id = await cursor.fetchone()
            await connection.commit()
            return module_id[0]
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Invalid company id")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Company module already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating company module {e}")

def delete_company_module(connection: Connection, company_module_id: List[int]) -> None:
    query = """
            DELETE FROM public.company_modules
            WHERE company_module_id = ANY(%s)
            RETURNING company_module_id;
            """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (company_module_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error deleting company module {e}")
        raise HTTPException(status_code=400, detail="Error deleting company module")

def get_company_modules(connection: Connection, column: str = None, value: str | int = None, row: str = None) -> List[Dict]:
    query = "SELECT * FROM public.company_modules "
    if row:
        query = f"SELECT {row} FROM public.company_modules "
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
        print(f"Error querying company modules {e}")
        raise HTTPException(status_code=400, detail="Error querying company modules")