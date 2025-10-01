from fastapi import HTTPException
from psycopg import AsyncConnection, sql



async def get_summary_findings(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL("SELECT * FROM public.issue WHERE engagement = %s;")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching issue based on engagement {e}")

async def get_summary_audit_process(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL(
        """
            SELECT 
            main_program.id,
            main_program.name,
            main_program.status,
            main_program.process_rating,
            COUNT(issue.id) AS issue_count,
            COUNT(CASE WHEN issue.risk_rating = 'Acceptable' THEN 1 END) AS acceptable,
            COUNT(CASE WHEN issue.risk_rating = 'Improvement Required' THEN 1 END) AS improvement_required,
            COUNT(CASE WHEN issue.risk_rating = 'Significant Improvement Required' THEN 1 END) AS significant_improvement_required,
            COUNT(CASE WHEN issue.risk_rating = 'Unacceptable' THEN 1 END) AS Unacceptable,
            COUNT(CASE WHEN issue.recurring_status = true THEN 1 END) AS recurring_issues
            FROM engagements 
            JOIN main_program ON main_program.engagement = engagements.id
            LEFT JOIN sub_program ON sub_program.program = main_program.id
            LEFT JOIN issue ON sub_program.id = issue.sub_program
            WHERE main_program.engagement = %s
            GROUP BY main_program.name, main_program.status, main_program.process_rating, main_program.id; 
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching summary of audit process {e}")

