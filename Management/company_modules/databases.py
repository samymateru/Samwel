from fastapi import HTTPException
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from Management.company_modules.schemas import *
from psycopg import AsyncConnection, sql
from utils import get_unique_key

async def add_new_company_module(connection: AsyncConnection, company_module: CompanyModule, company_id: str):
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

async def delete_company_module(connection: AsyncConnection, company_module_id: str):
    query = sql.SQL("""
            DELETE FROM public.company_modules
            WHERE company_module_id = ANY(%s)
            RETURNING company_module_id;
            """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_module_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting company module {e}")

async def get_company_modules(connection: AsyncConnection, company_id: str):
    query = sql.SQL("SELECT * FROM public.company_modules WHERE company = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying company modules {e}")