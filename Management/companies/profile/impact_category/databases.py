from fastapi import HTTPException
from psycopg import AsyncConnection, sql
from Management.companies.profile.impact_category.schemas import *

async def get_combined_impact_category(connection: AsyncConnection, company_id: str):
    query = sql.SQL(
        """
        SELECT
            imp.name AS process_name,
            ARRAY_AGG(sub.value) AS sub_process_name
        FROM
            impact_category imp
        JOIN
            impact_sub_category imps ON imps.impact_category = imp.id
        JOIN
            LATERAL unnest(imps.values) AS sub(value) ON TRUE
        WHERE
            imp.company = %s
        GROUP BY
            imp.id;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching combined impact categories {e}")