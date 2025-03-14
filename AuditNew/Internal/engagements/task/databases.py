import json
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.task.schemas import *
from utils import get_reference

def add_new_task(connection: Connection, task: NewTask, sub_program_id: int):
    query: str = """
                    INSERT INTO public.task (
                        sub_program,
                        title,
                        reference,
                        description,
                        date_raised,
                        raised_by,
                        action_owner,
                        resolution_summary,
                        resolution_details,
                        resolved_by,
                        date_resolved,
                        decision
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                 """
    try:
        reference: str = get_reference(connection=connection, resource="task", id=sub_program_id)
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                sub_program_id,
                reference,
                task.title,
                "",
                datetime.now(),
                json.dumps({
                    "id": 0,
                    "name": "",
                    "email": "example@gmail.com",
                    "date_issue": str(datetime.now())
                }),
                json.dumps({
                    "id": 0,
                    "name": "",
                    "email": "example@gmail.com",
                    "date_issue": str(datetime.now())
                }),
                "",
                "",
                json.dumps({
                    "id": 0,
                    "name": "",
                    "email": "example@gmail.com",
                    "date_issue": str(datetime.now())
                }),
                datetime.now(),
                ""
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
        task.raised_by,
        task.action_owner,
        task.resolution_summary,
        task.resolution_details,
        task.resolved_by,
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