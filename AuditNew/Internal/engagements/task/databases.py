import json
from fastapi import HTTPException
from AuditNew.Internal.engagements.task.schemas import *
from utils import get_reference, get_unique_key, check_row_exists
from psycopg import AsyncConnection, sql
from psycopg.errors import ForeignKeyViolation, UniqueViolation


async def raise_task(connection: AsyncConnection, task: NewTask, engagement_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.task (
            id,
            engagement,
            reference,
            title,
            description,
            raised_by,
            action_owner,
            status,
            href,
            due_date
            ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """)
    try:
        reference = await get_reference(connection=connection, resource="task", id=engagement_id)
        async with connection.cursor() as cursor:
            exists = await check_row_exists(connection=connection, table_name="task", filters={
                "title": task.title,
                "engagement": engagement_id
            })
            if exists:
                raise HTTPException(status_code=400, detail="Task already exists")
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                reference,
                task.title,
                task.description,
                task.raised_by.model_dump_json(),
                json.dumps(task.model_dump().get("action_owner")),
                "Pending",
                task.href,
                task.due_date
            ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Engagement id is invalid")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Task already exist")
    except HTTPException:
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating task {e}")


async def remove_task(connection: AsyncConnection, task_id: str):
    query = sql.SQL("DELETE FROM public.task WHERE id = %s;")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (task_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting task {e}")

async def resolve_task_(connection: AsyncConnection, task: ResolveTask, task_id: str):
    query = sql.SQL(
        """
           UPDATE public.task
           SET 
           resolution_summary = %s,
           resolution_details = %s,
           resolved_by = %s::jsonb,
           status = %s
           WHERE id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                task.resolution_summary,
                task.resolution_details,
                task.resolved_by.model_dump_json(),
                "Ongoing",
                task_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error resolving task {e}")

async def resolve_decision_(connection: AsyncConnection, task: TaskDecision, task_id: str):
    query = sql.SQL(
        """
           UPDATE public.task
           SET 
           decision = %s,
           status = %s
           WHERE id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                task.decision.value,
                "Pending" if task.decision.value == task.decision.RE_OPEN else "Closed",
                task_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error resolving task decision {e}")

async def update_task(connection:AsyncConnection, task:NewTask, task_id:str):
    query = sql.SQL(
        """
        UPDATE public.task
        SET 
        title = %s,
        description = %s,
        raised_by = %s::jsonb,
        href = %s,
        due_date = %s,
        action_owner = %s::jsonb
        WHERE id = %s
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                task.title,
                task.description,
                task.raised_by.model_dump_json(),
                task.href,
                task.due_date,
                json.dumps(task.model_dump().get("action_owner")),
                task_id
            ))
            await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error resolving review comment decision {e}")