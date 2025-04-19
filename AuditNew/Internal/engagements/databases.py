from fastapi import HTTPException
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from AuditNew.Internal.engagements.schemas import Engagement
import json
from psycopg import AsyncConnection
from psycopg import sql
from utils import get_unique_key

async def create_new_engagement(connection: AsyncConnection, engagement: Engagement, plan_id: str, code: str):
    query = sql.SQL(
        """
        INSERT INTO public.engagements (id, plan_id, code, name, risk, type, status, leads, stage, department,
        sub_departments, quarter, start_date, end_date, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query,
                           (
                               get_unique_key(),
                               plan_id,
                               code,
                               engagement.engagementName,
                               json.dumps(engagement.engagementRisk.model_dump()),
                               engagement.engagementType,
                               engagement.status,
                               json.dumps(engagement.model_dump().get("engagementLead")),
                               engagement.stage,
                               json.dumps(engagement.department.model_dump()),
                               json.dumps(engagement.sub_department),
                               engagement.plannedQuarter,
                               engagement.startDate,
                               engagement.endDate,
                               engagement.created_at
                           ))
            id = await cursor.fetchone()
            await connection.commit()
        return id[0]
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Invalid annual plan id")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Engagement already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating engagement {e}")

async def remove_engagements(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("DELETE FROM public.engagements WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting engagement {e}")


async def get_engagements(connection: AsyncConnection, annual_id: str):
    query = sql.SQL("SELECT * FROM public.engagements WHERE plan_id")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (annual_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagements {e}")

async def get_engagement_code(connection: AsyncConnection, annual_id: str):
    query = sql.SQL("SELECT code FROM public.engagements WHERE plan_id = %s;")

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (annual_id,))
            id_ = await cursor.fetchall()
            if id_ is None:
                return []
            return id_
    except Exception as e:
        await connection.rollback()
        print(e)
        #raise HTTPException(status_code=400, detail=f"Error fetching engagement code {e}")
        return []

def delete_engagement(connection: AsyncConnection, engagement_id: str):
    pass
