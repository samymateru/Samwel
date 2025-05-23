from fastapi import HTTPException
from psycopg import AsyncConnection, sql
from Management.entity.profile.risk_category.schemas import *

async def get_combined_risk_category(connection: AsyncConnection, company_id: str):
    query = sql.SQL(
        """
        SELECT
        rsk.name AS risk_category,
        ARRAY_AGG(sub.value) AS sub_risk_category
        FROM
            risk_category rsk
        JOIN
            sub_risk_category srk ON srk.risk_category = rsk.id
        JOIN
            LATERAL unnest(srk.values) AS sub(value) ON TRUE
        WHERE
            rsk.company = %s
        GROUP BY
        rsk.id;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching risk categories {e}")