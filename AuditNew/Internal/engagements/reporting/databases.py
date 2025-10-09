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
            mp.id AS main_program_id,
            mp.name AS program,
            COALESCE(
                json_agg(
                    json_build_object(
                         'sub_program_id', sp.id,
                         'title', sp.title,
                         'effectiveness', sp.effectiveness,
                         'issue_counts', COALESCE(risk_stats.counts, '{}'),
                         'total_very_high_risk', COALESCE(risk_stats.counts->>'very_high_risk', '0')::int,
                         'total_moderate_risk', COALESCE(risk_stats.counts->>'moderate_risk', '0')::int,
                         'total_recurring_issues', COALESCE(risk_stats.counts->>'recurring_count', '0')::int,
                         'status',
                            CASE
                                WHEN sp.prepared_by IS NOT NULL AND sp.reviewed_by IS NOT NULL THEN 'Reviewed'
                                WHEN sp.prepared_by IS NOT NULL AND sp.reviewed_by IS NULL THEN 'Prepared'
                                ELSE 'Pending'
                            END
                    )
                ) FILTER (WHERE sp.id IS NOT NULL),
                '[]'
            ) AS sub_programs
        FROM main_program mp
        LEFT JOIN sub_program sp ON sp.program = mp.id
        LEFT JOIN (
            SELECT 
                i.sub_program,
                json_build_object(
                    'total', COUNT(*) ,
                    'very_high_risk', COUNT(*) FILTER (WHERE i.risk_rating IN ('Significant Improvement Required', 'Unacceptable')),
                    'moderate_risk', COUNT(*) FILTER (WHERE i.risk_rating IN ('Improvement Required', 'Acceptable')),
                    'recurring_count', COUNT(*) FILTER (WHERE i.recurring_status = TRUE)
                ) AS counts
            FROM issue i
            GROUP BY i.sub_program
        ) AS risk_stats ON risk_stats.sub_program = sp.id
        WHERE mp.engagement = %s
        GROUP BY mp.id, mp.name
        ORDER BY mp.name;
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

