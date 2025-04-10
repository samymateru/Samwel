import json
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.review_comment.schemas import *
from utils import get_reference


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

def raise_review_comment_(connection: Connection, review_comment: NewReviewComment, engagement_id: int):
    query: str = """
                    INSERT INTO public.review_comment (
                        engagement,
                        reference,
                        title,
                        description,
                        raised_by,
                        action_owner
                        ) VALUES (%s, %s, %s, %s, %s, %s);
                 """
    try:
        reference: str = get_reference(connection=connection, resource="review_comment", id=engagement_id)
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                engagement_id,
                reference,
                review_comment.title,
                review_comment.description,
                review_comment.raised_by.model_dump_json(),
                json.dumps(review_comment.model_dump().get("action_owner"))
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error raising review comment {e}")

def resolve_review_comment_(connection: Connection, review_comment: ResolveReviewComment, review_comment_id: int):
    query: str = """
                   UPDATE public.review_comment
                   SET 
                   resolution_summary = %s,
                   resolution_details = %s,
                   resolved_by = %s::jsonb,
                   decision = %s
                   WHERE id = %s;
                 """
    try:
        reference: str = get_reference(connection=connection, resource="review_comment", id=engagement_id)
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (

            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error raising review comment {e}")
