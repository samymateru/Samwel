import json
from fastapi import HTTPException
from AuditNew.Internal.engagements.administration.schemas import *
from psycopg import AsyncConnection, sql
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from AuditNew.Internal.engagements.administration.schemas import __Staff__
from utils import get_unique_key

async def edit_engagement_profile(connection: AsyncConnection, profile: EngagementProfile, engagement_id: str):
    query = sql.SQL(
        """
        UPDATE public.profile
        SET 
            audit_background = %s::jsonb,
            audit_objectives = %s::jsonb,
            key_legislations = %s::jsonb ,
            relevant_systems = %s::jsonb,
            key_changes = %s::jsonb,
            reliance = %s::jsonb,
            scope_exclusion = %s::jsonb,
            core_risk = %s
            WHERE engagement = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
            json.dumps(profile.audit_background),
            json.dumps(profile.audit_objectives),
            json.dumps(profile.key_legislations),
            json.dumps(profile.relevant_systems),
            json.dumps(profile.key_changes),
            json.dumps(profile.reliance),
            json.dumps(profile.scope_exclusion),
            profile.core_risk,
            engagement_id
        ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Engagement id is invalid")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Profile already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating engagement profile {e}")

async def add_engagement_policies(connection: AsyncConnection, policy: Policy, engagement_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.policies (
            id,
            engagement,
            name,
            version,
            key_areas,
            attachment
        ) 
        VALUES(%s, %s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                policy.name,
                policy.version,
                policy.key_areas,
                policy.attachment
            ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Engagement id is invalid")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Policy already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement policy {e}")

async def add_new_business_contact(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.business_contact (
            id,
            engagement,
            "user",
            type
        ) 
        VALUES(%s, %s, %s::jsonb, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                json.dumps([]),
                "action"
            ))
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                json.dumps([]),
                "info"
            ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Engagement id is invalid")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding business contact {e}")

async def add_engagement_process(connection: AsyncConnection, process: EngagementProcess, engagement_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.engagement_process (
            id,
            engagement,
            process,
            sub_process,
            description,
            business_unit
        ) 
        VALUES(%s, %s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                process.process,
                process.sub_process,
                process.description,
                process.business_unit
            ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Engagement id is invalid")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Process already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement process {e}")

async def add_engagement_regulations(connection: AsyncConnection, regulation: Regulations, engagement_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.regulations (
            id,
            engagement,
            name,
            issue_date,
            key_areas,
            attachment
        ) 
        VALUES(%s, %s, %s, %s, %s, %s)
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                regulation.name,
                regulation.issue_date,
                regulation.key_areas,
                regulation.attachment
            ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Engagement id is invalid")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Regulation already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement regulation {e}")

async def add_engagement_staff(connection: AsyncConnection, staff: Staff, engagement_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.staff (
            id,
            engagement,
            name,
            email,
            role,
            start_date,
            end_date,
            tasks
        ) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        """)

    query_module_id = sql.SQL(
        """
        SELECT ap.module as module
        FROM engagements eng
        JOIN annual_plans ap ON ap.id = eng.plan_id
        WHERE eng.id = {engagement_id}
        """).format(engagement_id=sql.Literal(engagement_id))

    add_task_query = sql.SQL(
        """
        UPDATE modules
        SET users = (
        SELECT jsonb_agg(
        CASE
        WHEN item->>'id' = %s THEN
        jsonb_set(
            jsonb_set(item, '{engagements}', item->'engagements' || to_jsonb(%s::varchar[])),
            '{title}', to_jsonb(item->'title'::text)
            )              
            ELSE item
            END
            )
            FROM jsonb_array_elements(users) AS item
        )
        WHERE id = %s;
        """)

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                staff.name,
                staff.email,
                staff.role,
                staff.start_date,
                staff.end_date,
                staff.tasks
            ))
            await cursor.execute(query_module_id)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            module_id = [dict(zip(column_names, row_)) for row_ in rows]
            print(module_id[0].get("module"))
            await cursor.execute(add_task_query, (staff.user_id, [engagement_id], module_id[0].get("module")))
            await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Engagement id is invalid")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Staff already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding engagement staff {e}")

async def get_engagement_profile(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * from public.profile WHERE engagement = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement profile {e}")


async def get_business_contacts(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * from public.business_contact WHERE engagement = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching business contacts {e}")

async def get_engagement_policies(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * from public.policies WHERE engagement = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement policies {e}")

async def get_engagement_process(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * from public.engagement_process WHERE engagement = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement processes {e}")

async def get_engagement_regulations(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * from public.regulations WHERE engagement = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement regulations {e}")


async def get_engagement_staff(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * from public.staff WHERE engagement = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagement staffing {e}")

async def remove_profile(connection: AsyncConnection, profile_id: str):
    query = sql.SQL("DELETE FROM public.profile WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (profile_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting engagement profile {e}")


async def remove_policy(connection: AsyncConnection, policy_id: str):
    query = sql.SQL("DELETE FROM public.policies WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (policy_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error removing policy {e}")

async def remove_engagement_process(connection: AsyncConnection, engagement_process_id: str):
    query = sql.SQL("DELETE FROM public.engagement_process WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_process_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error removing engagement process {e}")


async def remove_staff(connection: AsyncConnection, staff_id: str):
    query = sql.SQL("DELETE FROM public.staff WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (staff_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error removing staff {e}")

async def remove_regulation(connection: AsyncConnection, regulation_id: str):
    query = sql.SQL("DELETE FROM public.regulations WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (regulation_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error removing regulation {e}")

async def edit_business_contact(connection: AsyncConnection, business_contact: BusinessContact, engagement_id: str):
    query = sql.SQL(
        """
          UPDATE public.business_contact
          SET 
          "user" = %s::jsonb
          WHERE engagement = %s AND type = %s
        """)
    try:
        async with connection.cursor() as cursor:

            await cursor.execute(query, (
                json.dumps(business_contact.model_dump().get("user")),
                engagement_id,
                business_contact.type
                ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Engagement id is invalid")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating business contact {e}")

async def edit_engagement_process(connection: AsyncConnection, engagement_process: EngagementProcess, engagement_process_id: str):
    query = sql.SQL(
        """
          UPDATE public.engagement_process
          SET 
          process = %s,
          sub_process = %s,
          description = %s,
          business_unit = %s
          WHERE id = %s
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                engagement_process.process,
                engagement_process.sub_process,
                engagement_process.description,
                engagement_process.business_unit,
                engagement_process_id
                ))
        await connection.commit()
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Process already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating engagement process {e}")

async def edit_regulations(connection: AsyncConnection, regulation: Regulations, regulation_id: str):
    query = sql.SQL(
        """
          UPDATE public.regulations
          SET 
          name = %s,
          issue_date = %s,
          key_areas = %s
          WHERE id = %s
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                regulation.name,
                regulation.issue_date,
                regulation.key_areas,
                regulation_id
                ))
        await connection.commit()
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Regulation already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating regulation {e}")

async def edit_policies(connection: AsyncConnection, policy: Policy, policy_id: str):
    query = sql.SQL(
    """
    UPDATE public.policies
    SET 
    name = %s,
    version = %s,
    key_areas = %s
    WHERE id = %s
    """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                policy.name,
                policy.version,
                policy.key_areas,
                policy_id))
        await connection.commit()
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Policy already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating policy {e}")

async def edit_staff(connection: AsyncConnection, staff: __Staff__, staff_id: str):
    query = sql.SQL(
        """
          UPDATE public.staff
          SET 
          role = %s,
          start_date = %s,
          end_date = %s
          WHERE id = %s
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                staff.role,
                staff.start_date,
                staff.end_date,
                staff_id
                ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Engagement id is invalid")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Staff already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating staffing {e}")