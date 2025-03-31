import json
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.review_comment.schemas import *
from utils import get_reference

def add_new_review_comment(connection: Connection, review_comment: ReviewComment, engagement_id: int):
    query: str = """
                    INSERT INTO public.review_comment (
                        engagement,
                        reference,
                        title,
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
        reference: str = get_reference(connection=connection, resource="review_comment", id=engagement_id)
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(
                engagement_id,
                reference,
                review_comment.title,
                review_comment.description,
                review_comment.date_raised,
                review_comment.raised_by.model_dump_json(),
                review_comment.action_owner.model_dump_json(),
                review_comment.resolution_summary,
                review_comment.resolution_details,
                review_comment.resolved_by.model_dump_json(),
                review_comment.date_resolved,
                review_comment.decision
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating review comment {e}")

def edit_review_comment(connection: Connection, review_comment: ReviewComment, review_comment_id: int):
    query = """
    UPDATE public.review_comment
    SET 
        title = %s,
        description = %s,
        date_raised = %s,
        raised_by = %s::jsonb,
        action_owner = %s::jsonb,
        resolution_summary = %s,
        resolution_details = %s,
        resolved_by = %s::jsonb,
        date_resolved = %s,
        decision = %s
    WHERE id = %s;
    """
    values = (
        review_comment.title,
        review_comment.description,
        review_comment.date_raised,
        review_comment.raised_by.model_dump_json(),
        review_comment.action_owner.model_dump_json(),
        review_comment.resolution_summary,
        review_comment.resolution_details,
        review_comment.resolved_by.model_dump_json(),
        review_comment.date_resolved,
        review_comment.decision,
        review_comment_id
    )
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating review note {e}")

def remove_review_comment(connection: Connection, review_comment_id: int):
    query: str = """
                  DELETE FROM public.review_comment WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(review_comment_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting review comment {e}")

