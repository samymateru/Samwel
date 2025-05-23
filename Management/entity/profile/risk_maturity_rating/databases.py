from fastapi import HTTPException
from Management.entity.profile.risk_maturity_rating.schemas import *
from psycopg import AsyncConnection, sql
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from utils import get_unique_key

async def new_risk_maturity_rating(connection: AsyncConnection, maturity_rating: RiskMaturityRating, company_id: str):
    query = sql.SQL("INSERT INTO public.risk_maturity_rating (id, company, name) VALUES(%s, %s, %s)")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                get_unique_key(),
                company_id,
                maturity_rating.name
            ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Invalid company id")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Maturity rating already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding risk maturity rating {e}")

async def delete_risk_maturity_rating(connection: AsyncConnection, maturity_rating_id: str):
    query = sql.SQL(
        """
        DELETE FROM public.risk_maturity_rating
        WHERE id = %s
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                maturity_rating_id,
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting risk maturity rating {e}")

async def edit_risk_maturity_rating(connection: AsyncConnection, maturity_rating: RiskMaturityRating, company_id: str):
    query = sql.SQL(
        """
        UPDATE public.risk_maturity_rating
        SET
        name = %s
        WHERE id = %s 
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                maturity_rating.name,
                company_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating risk maturity rating {e}")

async def get_company_risk_maturity_rating(connection: AsyncConnection , company_id: str):
    query = sql.SQL("SELECT * from public.risk_maturity_rating WHERE company = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching company risk maturity rating {e}")
