import json
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.task.schemas import *
from utils import get_reference

def raise_task(connection: Connection, task: NewTask, engagement_id: int):
    query: str = """
                    INSERT INTO public.task (
                        engagement,
                        reference,
                        title,
                        description,
                        date_raised,
                        raised_by,
                        action_owner
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
                 """
    try:
        reference: str = get_reference(connection=connection, resource="task", id=engagement_id)
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                engagement_id,
                reference,
                task.title,
                task.reference,
                task.date_raised,
                task.raised_by.model_dump_json(),
                json.dumps(task.model_dump().get("action_owner"))
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating task {e}")

def edit_task(connection: Connection, task: Task, task_id: int):
    query = """
    UPDATE public.task
    SET 
        title = %s,
        description = %s,
        date_raised = %s,
        raised_by = %s,
        action_owner = %s,
        resolution_summary = %s,
        resolution_details = %s,
        resolved_by = %s,
        date_resolved = %s,
        decision = %s
    WHERE id = %s;
    """
    values = (
        task.title,
        task.description,
        task.date_raised,
        task.raised_by.model_dump_json(),
        task.action_owner.model_dump_json(),
        task.resolution_summary,
        task.resolution_details,
        task.resolved_by.model_dump_json(),
        task.date_resolved,
        task.decision,
        task_id
    )
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating task {e}")

def remove_task(connection: Connection, task_id: int):
    query: str = """
                  DELETE FROM public.task WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (task_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting task {e}")
