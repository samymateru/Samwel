from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from fastapi import HTTPException
from collections import defaultdict
from psycopg import AsyncConnection, sql


async def get_combined_business_process(connection: AsyncConnection, company_id: str):
    query = sql.SQL(
        """
            SELECT
            bp.id as id,
            bp.name AS process_name,
            bp.code,
            ARRAY_AGG(sub.value) AS sub_process_name
            FROM
            business_process bp
            JOIN
            business_sub_process bsp ON bsp.business_process = bp.id
            JOIN
            LATERAL unnest(bsp.values) AS sub(value) ON TRUE
            WHERE
            bp.company = %s
            GROUP BY
            bp.id;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching business process: {e}")