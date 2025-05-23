from collections import defaultdict
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from fastapi import HTTPException
from Management.entity.profile.root_cause_category.schemas import *
from psycopg import AsyncConnection, sql

async def get_combined_root_cause_category(connection: AsyncConnection, company_id: str):
    query = sql.SQL(
        """
            SELECT
                rcc.name AS root_cause,
                ARRAY_AGG(sub.value) AS sub_root_cause
            FROM
                root_cause_category rcc
            JOIN
                root_Cause_sub_category rcsc ON rcsc.root_cause_Category = rcc.id
            JOIN
                LATERAL unnest(rcsc.values) AS sub(value) ON TRUE
            WHERE
                rcc.company = %s
            GROUP BY
        rcc.id;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching combined root cause {e}")