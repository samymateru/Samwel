from datetime import datetime

from fastapi import HTTPException
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from AuditNew.Internal.engagements.administration.databases import add_engagement_staff
from AuditNew.Internal.engagements.administration.schemas import Staff
from AuditNew.Internal.engagements.schemas import Engagement, UpdateEngagement
import json
from psycopg import AsyncConnection
from psycopg import sql

from Management.users.databases import get_module_users
from services.connections.postgres.read import ReadBuilder
from utils import get_unique_key, check_row_exists, exception_response


async def add_new_engagement(connection: AsyncConnection, engagement: Engagement, plan_id: str, code: str, module_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.engagements (id, plan_id, code, name, risk, type, status, leads, stage, department,
        sub_departments, quarter, start_date, end_date, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """)

    try:
        async with connection.cursor() as cursor:
            exists = await check_row_exists(connection=connection, table_name="engagements", filters={
                "name": engagement.name,
                "plan_id": plan_id
            })
            if exists:
                raise HTTPException(status_code=400, detail="Engagement already exists")
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
            users = await get_module_users(connection=connection, module_id=module_id)

            # if not any(user.get("role") == "Head of Audit" for user in users):
            #     raise HTTPException(status_code=400, detail="Head of Audit required")

            for user in users:
                if user.get("role") == "Head of Audit":
                    head = Staff(
                        user_id=user.get("id"),
                        name=user.get("name"),
                        email=user.get("email"),
                        role="Head of Audit",
                        start_date=datetime.now(),
                        end_date=datetime.now()
                    )
                    await add_engagement_staff(
                        connection=connection,
                        staff=head,
                        engagement_id=engagement_id[0]
                    )
            for lead in engagement.leads:
                staff = Staff(
                    user_id=lead.id,
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
    except HTTPException:
        raise
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


async def get_engagements(connection: AsyncConnection, annual_id: str, email: str):
    query = sql.SQL("SELECT * FROM public.engagements WHERE plan_id = %s AND id = ANY(%s);")
    query_engagements = sql.SQL(
        """
        SELECT engagement FROM public.staff WHERE email = %s;
        """)

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query=query_engagements, params=(email,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            engagement_ids = [dict(zip(column_names, row_)) for row_ in rows]
            engagement_list = [item['engagement'] for item in engagement_ids]
            await cursor.execute(query=query, params=(annual_id, engagement_list))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except HTTPException:
        raise
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

async def edit_engagement(connection: AsyncConnection, engagement: UpdateEngagement, engagement_id: str):
    get_code_query = sql.SQL(
        """
        SELECT code FROM public.engagements WHERE id = {engagement_id}
        """).format(engagement_id=sql.Literal(engagement_id))

    query = sql.SQL(
        """
        UPDATE public.engagements
        SET
        name = %s,
        type = %s,
        code = %s,
        department = %s::jsonb,
        sub_departments = %s,
        risk = %s::jsonb
        WHERE id = %s
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(get_code_query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            engagement_code = [dict(zip(column_names, row_)) for row_ in rows]
            code_string: str = engagement_code[0].get("code", "")
            data = code_string.split("-")
            data[0] = engagement.department.code
            await cursor.execute(query, (
                engagement.name,
                engagement.type,
                "-".join(data),
                engagement.department.model_dump_json(),
                json.dumps(engagement.sub_departments),
                engagement.risk.model_dump_json(),
                engagement_id
                ))
            await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating engagement {e}")


async def get_completed_engagement(connection: AsyncConnection, module_id: str):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table("annual_plans", alias="ap")
            .join(
                "LEFT",
                on="ap.id = engagement.plan_id",
                table="engagements",
                alias="engagement",
                use_prefix=True
            )
            .where("module", module_id)
            .where("engagement.status", "Completed")
            .fetch_all()
        )
        return builder

