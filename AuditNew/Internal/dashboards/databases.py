from collections import Counter

from fastapi import HTTPException
from psycopg import AsyncConnection, sql
from datetime import datetime

from AuditNew.Internal.dashboards.schemas import _Engagement_, ModuleHomeDashboard, _Issue_, _EngagementStatus_


async def query_annual_plans_summary(
        connection: AsyncConnection,
        company_module_id:str,
        start_year: str = None,
        end_year: str = None,
        year: str = None
):
    base_query = sql.SQL("""
        SELECT
            annual_plans.year,
            COUNT(*) AS total,
            COUNT(*) FILTER (WHERE status = 'Not Started') AS not_started,
            COUNT(*) FILTER (WHERE status = 'In progress') AS in_progress,
            COUNT(*) FILTER (WHERE status = 'Completed') AS completed
        FROM annual_plans
        WHERE company_module = {company_module}
    """).format(
        company_module=sql.Literal(company_module_id)
    )

    conditions = []

    if start_year and end_year:
        conditions.append(
            sql.SQL("year BETWEEN {start} AND {end}").format(
                start=sql.Literal(start_year),
                end=sql.Literal(end_year)
            )
        )
    elif year:
        conditions.append(
            sql.SQL("year = {year}").format(
                year=sql.Literal(year)
            )
        )

    if conditions:
        base_query += sql.SQL(" AND ") + sql.SQL(" AND ").join(conditions)

    base_query += sql.SQL(" GROUP BY annual_plans.year ORDER BY annual_plans.year;")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(base_query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            audit_plan_data = [dict(zip(column_names, row_)) for row_ in rows]
            return audit_plan_data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching summary of annual plans {e}")

async def query_audit_summary(
        connection: AsyncConnection,
        company_module_id: str,
        start_year: str = None,
        end_year: str = None,
        year: str = None
):
    query = sql.SQL(
        """
        SELECT jsonb_build_object(
            'total', COUNT(*),
            'pending', COUNT(*) FILTER (WHERE status = 'Pending'),
            'ongoing', COUNT(*) FILTER (WHERE status = 'Ongoing'),
            'completed', COUNT(*) FILTER (WHERE status = 'Completed')
        ) AS annual_plans_summary
        FROM annual_plans ap
        WHERE ap.module = {company_module};
        """).format(
        company_module=sql.Literal(company_module_id)
    )
    conditions = []

    if start_year and end_year:
        conditions.append(
            sql.SQL("year BETWEEN {start} AND {end}").format(
                start=sql.Literal(start_year),
                end=sql.Literal(end_year)
            )
        )
    elif year:
        conditions.append(
            sql.SQL("year = {year}").format(
                year=sql.Literal(year)
            )
        )

    if conditions:
        query += sql.SQL(" AND ") + sql.SQL(" AND ").join(conditions)

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            audit_plan_data = [dict(zip(column_names, row_)) for row_ in rows]
            if audit_plan_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="No audit plans found")
            return audit_plan_data[0]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching audit plans {e}")

async def all_engagement_with_status(connection: AsyncConnection, plan_id: str):
    query = sql.SQL(
        """
        SELECT jsonb_build_object(
            'total', COUNT(*),
            'not_started', COUNT(*) FILTER (WHERE status = 'Not started'),
            'in_progress', COUNT(*) FILTER (WHERE status = 'In progress'),
            'completed', COUNT(*) FILTER (WHERE status = 'Completed')
        ) AS engagements
        FROM engagements
        WHERE plan_id = {plan_id};
        """
    ).format(plan_id=sql.Literal(plan_id))
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            if data.__len__() == 0:
                raise HTTPException(status_code=400, detail="No engagements found")
            return data[0]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagements {e}")


async def all_engagement_summary(connection: AsyncConnection, company_module_id: str):
    query = sql.SQL(
        """
        SELECT jsonb_build_object(
            'total', COUNT(*),
            'pending', COUNT(*) FILTER (WHERE eng.status = 'Pending'),
            'ongoing', COUNT(*) FILTER (WHERE eng.status = 'Ongoing'),
            'completed', COUNT(*) FILTER (WHERE eng.status = 'Completed')
        ) AS engagements_summary
        FROM engagements eng
        JOIN annual_plans ap ON ap.id = eng.plan_id
        JOIN modules m ON m.id = ap.module
        WHERE m.id = {company_module_id};
        """
    ).format(company_module_id=sql.Literal(company_module_id))
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            if data.__len__() == 0:
                raise HTTPException(status_code=400, detail="No engagements found")
            return data[0]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching engagements {e}")

async def query_all_issues(connection: AsyncConnection, company_module_id: str):
    query = sql.SQL(
        """
        SELECT 
        -- Total issue count
        COUNT(*) FILTER (WHERE issue.status != 'Not started') AS total_issues,
  
        -- Recurring counts
        jsonb_build_object(
        'yes', COUNT(*) FILTER (WHERE issue.recurring_status = TRUE AND issue.status != 'Not started'),
        'no', COUNT(*) FILTER (WHERE issue.recurring_status = FALSE AND issue.status != 'Not started')
        )AS recurring_summary,
        
        --Issue status
        jsonb_build_object(
        'open', COUNT(*) FILTER (WHERE issue.status = 'Open' AND issue.status != 'Not started'),
        
        'in_progress', COUNT(*) FILTER (WHERE issue.status 
        IN ('In progress -> implementer', 'In progress -> owner') 
        AND issue.status != 'Not started'),
        
        'closed', COUNT(*) FILTER (WHERE issue.status 
        IN ('Closed -> not verified', 'Closed -> verified by risk',
        'Closed -> risk N/A', 'Closed -> risk accepted', 'Closed -> verified by audit')
        AND issue.status != 'Not started')
        )AS status_summary,

        -- Impact category counts
        (
        SELECT jsonb_object_agg(impact_category, count)
        FROM (
          SELECT issue.impact_category, COUNT(*) FILTER (WHERE issue.status != 'Not started') AS count
          FROM issue
          JOIN engagements ON issue.engagement = engagements.id
          JOIN annual_plans ON engagements.plan_id = annual_plans.id
          JOIN modules ON annual_plans.module = modules.id
          WHERE modules.id = %s
          GROUP BY issue.impact_category
          HAVING COUNT(*) FILTER (WHERE issue.status != 'Not started') > 0
        ) AS impact
        ) AS impact_summary,

        -- Business processes
        (
        SELECT jsonb_object_agg(process, count)
        FROM (
          SELECT issue.process, COUNT(*) FILTER (WHERE issue.status != 'Not started') AS count
          FROM issue
          JOIN engagements ON issue.engagement = engagements.id
          JOIN annual_plans ON engagements.plan_id = annual_plans.id
          JOIN modules ON annual_plans.module = modules.id
          WHERE modules.id = %s
          GROUP BY issue.process
          HAVING COUNT(*) FILTER (WHERE issue.status != 'Not started') > 0
          ORDER BY count DESC
          LIMIT 5
        ) AS process
        ) AS process_summary,

        -- Root cause
        (
        SELECT jsonb_object_agg(root_cause, count)
        FROM (
          SELECT issue.root_cause, COUNT(*) FILTER (WHERE issue.status != 'Not started') AS count
          FROM issue
          JOIN engagements ON issue.engagement = engagements.id
          JOIN annual_plans ON engagements.plan_id = annual_plans.id
          JOIN modules ON annual_plans.module = modules.id
          WHERE modules.id = %s
          GROUP BY issue.root_cause   
          HAVING COUNT(*) FILTER (WHERE issue.status != 'Not started') > 0
	    ) AS root_cause
        ) AS root_cause_summary
  
        FROM issue
        JOIN engagements ON issue.engagement = engagements.id
        JOIN annual_plans ON engagements.plan_id = annual_plans.id
        JOIN modules ON annual_plans.module = modules.id
        WHERE modules.id = %s;
        """
    )
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_module_id, company_module_id, company_module_id,company_module_id))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            audit_plan_data = [dict(zip(column_names, row_)) for row_ in rows]
            if audit_plan_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="Cant provide issue details check the module id")
            return audit_plan_data[0]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching issue details {e}")


async def query_planning_details(connection: AsyncConnection, plan_id: str):
    query = sql.SQL(
        """
        SELECT
        jsonb_build_object(
            'total', COUNT(*),
            'pending', COUNT(*) FILTER (WHERE eng.status = 'Pending'),
            'ongoing', COUNT(*) FILTER (WHERE eng.status = 'Ongoing'),
            'completed', COUNT(*) FILTER (WHERE eng.status = 'Completed')
        ) AS planning_summary

        FROM engagements eng
        WHERE eng.plan_id = %s;
        """
    )
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (plan_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            audit_plan_data = [dict(zip(column_names, row_)) for row_ in rows]
            if audit_plan_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="Cant provide planning details check the module id")
            return audit_plan_data[0]

    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching planning details {e}")

async def query_engagement_details(connection: AsyncConnection, engagement_id: str):
    query_procedures = sql.SQL(
        """
        WITH finalization_summary AS (
        SELECT
        COUNT(*) AS total_finalization_procedures,
        jsonb_build_object(
            'pending', COUNT(*) FILTER (WHERE fp.prepared_by IS NULL AND fp.reviewed_by IS NULL),
            'in_progress', COUNT(*) FILTER (WHERE fp.prepared_by IS NOT NULL AND fp.reviewed_by IS NULL),
            'completed', COUNT(*) FILTER (WHERE fp.prepared_by IS NOT NULL AND fp.reviewed_by IS NOT NULL)
        ) AS finalization_status_summary
        FROM finalization_procedure fp
        JOIN engagements e ON fp.engagement = e.id
        WHERE e.id = {engagement_id}
        ),
        reporting_summary AS (
        SELECT
        COUNT(*) AS total_reporting_procedures,
        jsonb_build_object(
            'pending', COUNT(*) FILTER (WHERE rp.prepared_by IS NULL AND rp.reviewed_by IS NULL),
            'in_progress', COUNT(*) FILTER (WHERE rp.prepared_by IS NOT NULL AND rp.reviewed_by IS NULL),
            'completed', COUNT(*) FILTER (WHERE rp.prepared_by IS NOT NULL AND rp.reviewed_by IS NOT NULL)
        ) AS report_status_summary
        FROM reporting_procedure rp
        JOIN engagements e ON rp.engagement = e.id
        WHERE e.id = {engagement_id}
        ),
        planning_summary AS (
        SELECT
        COUNT(*) AS total_planning_procedures,
        jsonb_build_object(
            'pending', COUNT(*) FILTER (WHERE tmp.prepared_by IS NULL AND tmp.reviewed_by IS NULL),
            'in_progress', COUNT(*) FILTER (WHERE tmp.prepared_by IS NOT NULL AND tmp.reviewed_by IS NULL),
            'completed', COUNT(*) FILTER (WHERE tmp.prepared_by IS NOT NULL AND tmp.reviewed_by IS NOT NULL)
        ) AS planning_status_summary
        FROM std_template tmp
        JOIN engagements e ON tmp.engagement = e.id
        WHERE e.id = {engagement_id}
        ),
        work_program_summary AS (
	    SELECT
	    COUNT(*) AS total_work_program_procedures,
	    jsonb_build_object(
	        'pending', COUNT(*) FILTER (WHERE sp.prepared_by IS NULL AND sp.reviewed_by IS NULL),
	        'in_progress', COUNT(*) FILTER (WHERE sp.prepared_by IS NOT NULL AND sp.reviewed_by IS NULL),
	        'completed', COUNT(*) FILTER (WHERE sp.prepared_by IS NOT NULL AND sp.reviewed_by IS NOT NULL)
	    ) AS work_program_procedure_status_summary
	    FROM main_program mp
	    JOIN engagements e ON mp.engagement = e.id
	    JOIN sub_program sp ON sp.program = mp.id
	    WHERE e.id = {engagement_id}
        )
        SELECT
        fs.total_finalization_procedures,
        fs.finalization_status_summary,
        rs.total_reporting_procedures,
        rs.report_status_summary,
	    ps.total_planning_procedures,
        ps.planning_status_summary,
	    wp.total_work_program_procedures,
	    wp.work_program_procedure_status_summary
        FROM 
	    finalization_summary fs, 
	    reporting_summary rs, 
	    planning_summary ps,
	    work_program_summary wp;
        """
    ).format(engagement_id=sql.Literal(engagement_id))

    query_root_cause_rating = sql.SQL(
        """
        SELECT
        COUNT(*) FILTER (WHERE i.status != 'Not started') AS total_issues,

        -- Root cause summary as JSON
        (
        SELECT jsonb_object_agg(root_cause, count)
        FROM (
            SELECT i.root_cause, COUNT(*) FILTER (WHERE i.status != 'Not started') AS count
            FROM issue i
            JOIN engagements e ON i.engagement = e.id
            WHERE e.id = {engagement_id}
            GROUP BY i.root_cause
            HAVING COUNT(*) FILTER (WHERE i.status != 'Not started') > 0
        ) AS root_cause_summary
        ) AS root_cause_summary,

        -- Risk rating summary as JSON
        (
        SELECT jsonb_object_agg(risk_rating, count)
        FROM (
            SELECT i.risk_rating, COUNT(*) FILTER (WHERE i.status != 'Not started') AS count
            FROM issue i
            JOIN engagements e ON i.engagement = e.id
            WHERE e.id = {engagement_id}
            GROUP BY i.risk_rating
            HAVING COUNT(*) FILTER (WHERE i.status != 'Not started') > 0
        ) AS rating_summary
        ) AS risk_rating_summary

        FROM issue i
        JOIN engagements e ON i.engagement = e.id
        WHERE e.id = {engagement_id};
        """).format(engagement_id=sql.Literal(engagement_id))

    query_review_comment = sql.SQL(
        """
        SELECT
        jsonb_build_object(
            'pending', COUNT(*) FILTER (WHERE rc.status = 'Pending'),
            'in_progress', COUNT(*) FILTER (WHERE rc.status = 'Ongoing'),
            'closed', COUNT(*) FILTER (WHERE rc.status = 'Closed'),
            'total', COUNT(*)
        ) as review_status
        
        FROM review_comment rc
        JOIN engagements e ON rc.engagement = e.id
        WHERE e.id = {engagement_id}
        """).format(engagement_id=sql.Literal(engagement_id))
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query_procedures)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            procedure_data = [dict(zip(column_names, row_)) for row_ in rows]
            if procedure_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="No data found")
            data = procedure_data[0]
            total_procedure = data.get("total_finalization_procedures") + data.get("total_reporting_procedures") + \
                              data.get("total_planning_procedures") + data.get("total_work_program_procedures")

            total_pending = data.get("finalization_status_summary").get("pending") + data.get(
                "report_status_summary").get("pending") + \
                            data.get("planning_status_summary").get("pending") + data.get(
                "work_program_procedure_status_summary").get("pending")

            total_in_progress = data.get("finalization_status_summary").get("in_progress") + data.get(
                "report_status_summary").get("in_progress") + \
                                data.get("planning_status_summary").get("in_progress") + data.get(
                "work_program_procedure_status_summary").get("in_progress")

            total_completed = data.get("finalization_status_summary").get("completed") + data.get(
                "report_status_summary").get("completed") + \
                              data.get("planning_status_summary").get("completed") + data.get(
                "work_program_procedure_status_summary").get("completed")
            engagement_data = {
                "total_procedure": total_procedure,
                "pending": total_pending,
                "in_progress": total_in_progress,
                "completed": total_completed
            }
            await cursor.execute(query_root_cause_rating)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            root_cause_rating_data = [dict(zip(column_names, row_)) for row_ in rows]
            if root_cause_rating_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="No data found")

            await cursor.execute(query_review_comment)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            review_comment_data = [dict(zip(column_names, row_)) for row_ in rows]
            if root_cause_rating_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="No data found")

            return {
                "procedure_summary": engagement_data,
                "issue_details": root_cause_rating_data[0],
                "review_comment": review_comment_data[0].get("review_status")
            }
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching planning details {e}")

async def get_modules_dashboard(connection: AsyncConnection, module_id: str):
    query_current_plan_engagements = sql.SQL(
        """
        SELECT
        eng.id AS engagement_id,
        eng.name AS engagement_name,
        eng.code AS engagement_code,
        eng.status AS engagement_status,
        eng.type AS engagement_type,
        eng.start_date AS engagement_start_date,
        eng.end_date AS engagement_end_date,
        eng.stage AS engagement_stage,
        
        isu.id AS issue_id,
        isu.ref AS issue_reference,
        isu.title AS issue_title,
        isu.finding AS issue_finding,
        isu.risk_rating AS issue_rating,
        isu.process AS issue_process
        
        FROM public.annual_plans pln
        JOIN public.engagements eng ON pln.id = eng.plan_id
        LEFT JOIN public.issue isu ON eng.id = isu.engagement
        WHERE pln.module = %s AND pln.year = %s
        ORDER BY eng.id, isu.id
        LIMIT 5;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query_current_plan_engagements, (
                module_id,
                str(datetime.now().year)
            ))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]

            dashboard_data = separate_engagements_and_issues(data)
            engagements_metrics = count_engagement_statuses(data)

            engagements = [_Engagement_(**eng) for eng in dashboard_data.get("engagements", [])]
            issues = [_Issue_(**eng) for eng in dashboard_data.get("issues", [])]

            final_data = ModuleHomeDashboard(
                engagements=engagements,
                engagements_metrics=engagements_metrics,
                issues=issues,
            )

            return final_data

    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error querying module home dashboard {e}")


def separate_engagements_and_issues(rows):
    engagements_dict = {}
    issues_dict = {}

    for row in rows:
        # Extract engagement fields
        engagement_id = row['engagement_id']
        if engagement_id not in engagements_dict:
            engagements_dict[engagement_id] = {
                'id': engagement_id,
                'name': row['engagement_name'],
                'code': row['engagement_code'],
                'status': row['engagement_status'],
                'type': row['engagement_type'],
                'start_date': row['engagement_start_date'],
                'end_date': row['engagement_end_date'],
                'stage': row['engagement_stage'],
            }

        # Extract issue fields
        issue_id = row['issue_id']
        if issue_id and issue_id not in issues_dict:
            issues_dict[issue_id] = {
                'id': issue_id,
                'reference': row['issue_reference'],
                'title': row['issue_title'],
                'finding': row['issue_finding'],
                'risk_rating': row['issue_rating'],
                'process': row['issue_process'],
                'engagement': engagement_id
            }

    return {
        "engagements": list(engagements_dict.values()),
        "issues": list(issues_dict.values())
    }


def count_engagement_statuses(rows):
    status_counter = Counter()

    for row in rows:
        status = row['engagement_status']
        if status:
            status_counter[status] += 1

    return _EngagementStatus_(
        total=sum(status_counter.values()),
        pending=status_counter.get("Pending", 0),
        ongoing=status_counter.get("Ongoing", 0),
        completed=status_counter.get("Completed", 0)
    )



