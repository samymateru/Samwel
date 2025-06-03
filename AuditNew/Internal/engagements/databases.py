from datetime import datetime

from fastapi import HTTPException
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from AuditNew.Internal.engagements.administration.databases import add_engagement_staff
from AuditNew.Internal.engagements.administration.schemas import Staff
from AuditNew.Internal.engagements.schemas import Engagement
import json
from psycopg import AsyncConnection
from psycopg import sql
from utils import get_unique_key

async def add_new_engagement(connection: AsyncConnection, engagement: Engagement, plan_id: str, code: str):
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
               engagement.name,
               json.dumps(engagement.risk.model_dump()),
               engagement.type,
               engagement.status,
               json.dumps(engagement.model_dump().get("leads")),
               engagement.stage,
               json.dumps(engagement.department.model_dump()),
               json.dumps(engagement.sub_departments),
               engagement.quarter,
               engagement.start_date,
               engagement.end_date,
               engagement.created_at
            ))
            engagement_id = await cursor.fetchone()
            await connection.commit()
            for lead in engagement.leads:
                staff = Staff(
                    name = lead.name,
                    email= lead.email,
                    role= "Lead",
                    start_date = datetime.now(),
                    end_date = datetime.now()
                )
                await add_engagement_staff(
                    connection=connection,
                    staff=staff,
                    engagement_id=engagement_id[0]
                )
            await connection.commit()
        return engagement_id[0]
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
    query = sql.SQL("SELECT * FROM public.engagements WHERE plan_id = %s")
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
