from fastapi import HTTPException
from psycopg import AsyncConnection, sql

from core.tables import Tables
from schemas.annual_plan_schemas import ReadAnnualPlan
from schemas.engagement_schemas import Engagement
from schemas.issue_schemas import IssueColumns, ReadIssues
from services.connections.postgres.read import ReadBuilder
from utils import exception_response


async def get_review_comments_report(connection: AsyncConnection, company_module_id: str):
    query = sql.SQL(
        """
        SELECT 
        rc.id,
        rc.title,
        rc.reference,
        rc.description,
        rc.raised_by,
        rc.resolution_summary,
        rc.resolution_details,
        rc.resolved_by,
        rc.decision,
        rc.status,
        rc.href
        FROM review_comment rc
        JOIN engagements en ON rc.engagement = en.id
        JOIN annual_plans ap ON en.plan_id = ap.id
        JOIN modules m ON ap.module = m.id
        WHERE m.id = %s
        GROUP BY
        rc.id,
        rc.title,
        rc.reference,
        rc.description,
        rc.raised_by,
        rc.resolution_summary,
        rc.resolution_details,
        rc.resolved_by,
        rc.decision,
        rc.status,
        rc.href
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_module_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            audit_plan_data = [dict(zip(column_names, row_)) for row_ in rows]
            return audit_plan_data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching review comments {e}")


async def get_tasks_report(connection: AsyncConnection, company_module_id: str):
    query = sql.SQL(
        """
        SELECT
        rc.id, 
        rc.title,
        rc.reference,
        rc.description,
        rc.raised_by,
        rc.resolution_summary,
        rc.resolution_details,
        rc.resolved_by,
        rc.decision,
        rc.status,
        rc.href
        FROM task rc
        JOIN engagements en ON rc.engagement = en.id
        JOIN annual_plans ap ON en.plan_id = ap.id
        JOIN modules m ON ap.module = m.id
        WHERE m.id = %s
        GROUP BY
        rc.id,
        rc.title,
        rc.reference,
        rc.description,
        rc.raised_by,
        rc.resolution_summary,
        rc.resolution_details,
        rc.resolved_by,
        rc.decision,
        rc.status,
        rc.href
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_module_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            audit_plan_data = [dict(zip(column_names, row_)) for row_ in rows]
            return audit_plan_data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching review comments {e}")



async def get_all_issue_reports(
        connection: AsyncConnection,
        module_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ISSUES.value, alias="iss")
            .select(ReadIssues)
            .join(
                "LEFT",
                Tables.ENGAGEMENTS.value,
                "engagement.id = iss.engagement",
                "engagement",
                use_prefix=True,
                model=Engagement
            )
            .join(
                "LEFT",
                Tables.ANNUAL_PLANS.value,
                "plan.id = engagement.plan_id",
                "plan",
                use_prefix=True,
                model=ReadAnnualPlan
            )
            .select_joins()
            .where("iss."+IssueColumns.MODULE_ID.value, module_id)
            .fetch_all()
        )

        return builder



