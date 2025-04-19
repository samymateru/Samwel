from fastapi import HTTPException
from Management.companies.profile.control_weakness_rating.schemas import *
from psycopg import AsyncConnection, sql


async def new_control_weakness_rating(connection: AsyncConnection, control_weakness_rating: ControlWeaknessRating, company_id: str):
    pass

async def delete_control_weakness_rating(connection: AsyncConnection, company_id: str):
    pass


async def edit_control_weakness_rating(connection: AsyncConnection, control_weakness_rating: ControlWeaknessRating, company_id: str):
    pass


async def get_company_control_weakness_rating(connection: AsyncConnection, company_id: str):
    query = sql.SQL("SELECT * from public.control_weakness_rating WHERE company = %s ")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching company control weakness rating {e}")
