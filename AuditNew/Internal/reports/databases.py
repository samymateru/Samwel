from typing import List
from fastapi import HTTPException
from psycopg import AsyncConnection, sql
from core.tables import Tables
from schemas.annual_plan_schemas import ReadAnnualPlan
from schemas.engagement_schemas import Engagement
from schemas.issue_schemas import IssueColumns, ReadIssues
from services.connections.postgres.read import ReadBuilder
from utils import exception_response
from collections import Counter
from typing import List
from AuditNew.Internal.dashboards.schemas import _Issue_, IssueStatusSummary

async def get_review_comments_report(connection: AsyncConnection, company_module_id: str):
    query = sql.SQL(
        """
        SELECT 
        rc.id,
        rc.title,
        rc.reference,
        rc.description,
        rc.raised_by,
        rc.action_owner,
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
        rc.action_owner,
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
        rc.action_owner,
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
        rc.action_owner,
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
            .where_raw("iss.status NOT IN ('Not started')")
            .fetch_all()
        )

        return builder



def count_issue_statuses(rows: List[_Issue_]):
    status_counter = Counter()

    for row in rows:

        # Normalize status into broader categories
        if row.status == "Not started":
            status_counter["Not started"] += 1
        elif row.status == "Open":
            status_counter["Open"] += 1
        elif row.status.startswith("In progress"):
            status_counter["In Progress"] += 1
        elif row.status.startswith("Closed"):
            status_counter["Closed"] += 1

    return IssueStatusSummary(
        total=sum(status_counter.values()),
        not_started=status_counter.get("Not started", 0),
        open=status_counter.get("Open", 0),
        in_progress=status_counter.get("In Progress", 0),
        closed=status_counter.get("Closed", 0),
    )




