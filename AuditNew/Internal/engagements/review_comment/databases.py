import json
from fastapi import HTTPException
from AuditNew.Internal.engagements.review_comment.schemas import *
from utils import get_reference, get_unique_key, check_row_exists
from psycopg import AsyncConnection, sql
from psycopg.errors import ForeignKeyViolation, UniqueViolation


async def remove_review_comment(connection: AsyncConnection, review_comment_id: str):
    query = sql.SQL("DELETE FROM public.review_comment WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query,(review_comment_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting review comment {e}")

async def raise_review_comment_(connection: AsyncConnection, review_comment: NewReviewComment, engagement_id: str):
    query = sql.SQL(
        """
        INSERT INTO public.review_comment (
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
        reference: str = await get_reference(connection=connection, resource="review_comment", __id__=engagement_id)
        async with connection.cursor() as cursor:
            exists = await check_row_exists(connection=connection, table_name="review_comment", filters={
                "title": review_comment.title,
                "engagement": engagement_id
            })
            if exists:
                raise HTTPException(status_code=400, detail="Review Comment already exists")
            await cursor.execute(query, (
                get_unique_key(),
                engagement_id,
                reference,
                review_comment.title,
                review_comment.description,
                review_comment.raised_by.model_dump_json(),
                json.dumps(review_comment.model_dump().get("action_owner")),
                "Pending",
                review_comment.href,
                review_comment.due_date
            ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Engagement id is invalid")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Review comment already exits")
    except HTTPException:
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error raising review comment {e}")

async def resolve_review_comment_(connection: AsyncConnection, review_comment: ResolveReviewComment, review_comment_id: str):
    query = sql.SQL(
        """
           UPDATE public.review_comment
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
                review_comment.resolution_summary,
                review_comment.resolution_details,
                review_comment.resolved_by.model_dump_json(),
                "Ongoing",
                review_comment_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error resolving review comment {e}")

async def review_comment_decision_(connection: AsyncConnection, review_comment: ReviewCommentDecision, review_comment_id: str):
    query = sql.SQL(
        """
           UPDATE public.review_comment
           SET 
           decision = %s,
           status = %s
           WHERE id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
                review_comment.decision.value,
                "Pending" if review_comment.decision.value == review_comment.decision.RE_OPEN else "Closed",
                review_comment_id
            ))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error resolving review comment decision {e}")

async def update_review_comment(connection:AsyncConnection, review_comment:NewReviewComment, review_comment_id:str):
    query = sql.SQL(
        """
        UPDATE public.review_comment
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
                review_comment.title,
                review_comment.description,
                review_comment.raised_by.model_dump_json(),
                review_comment.href,
                review_comment.due_date,
                json.dumps(review_comment.model_dump().get("action_owner")),
                review_comment_id
            ))
            await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error resolving review comment decision {e}")