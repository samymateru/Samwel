from fastapi import HTTPException
from psycopg import AsyncConnection, sql


async def get_summary_procedures(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL(
        """ 
        SELECT 
        main_program.name AS program, 
        sub_program.reference,
        sub_program.title,
        sub_program.prepared_by,
        sub_program.reviewed_by,
        sub_program.effectiveness,
        COUNT(issue.id) AS issue_count 
        FROM sub_program 
        LEFT JOIN main_program ON main_program.id = sub_program.program
        LEFT JOIN issue ON sub_program.id = issue.sub_program
        WHERE main_program.engagement = %s
        GROUP BY 
        main_program.name,
        sub_program.reference, 
        sub_program.title, 
        sub_program.prepared_by, 
        sub_program.reviewed_by, 
        sub_program.effectiveness; 
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching summary of procedures {e}")

async def get_summary_review_notes(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL(
        """
        SELECT 
        review_comment.id,
        review_comment.reference,
        review_comment.title,
        review_comment.description,
        review_comment.raised_by,
        review_comment.action_owner,
        review_comment.resolution_summary,
        review_comment.resolution_details,
        review_comment.resolved_by,
        review_comment.decision,
        review_comment.status
        FROM review_comment 
        WHERE engagement = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching summary of review notes {e}")

async def get_summary_task(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL(
        """
        SELECT 
        task.id,
        task.reference,
        task.title,
        task.description,
        task.raised_by,
        task.action_owner,
        task.resolution_summary,
        task.resolution_details,
        task.resolved_by,
        task.decision,
        task.status
        FROM task 
        WHERE engagement = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching summary of task {e}")
