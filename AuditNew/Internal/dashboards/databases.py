from fastapi import HTTPException
from psycopg import AsyncConnection, sql

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
            'not_started', COUNT(*) FILTER (WHERE status = 'Not Started'),
            'in_progress', COUNT(*) FILTER (WHERE status = 'In progress'),
            'completed', COUNT(*) FILTER (WHERE status = 'Completed')
        ) AS annual_plans
        FROM annual_plans
        WHERE company_module = {company_module};
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


async def query_all_issues(connection: AsyncConnection, company_module_id: str):
    query = sql.SQL(
        """
        SELECT 
        -- Total issue count
        COUNT(*) AS total_issues,
  
        -- Recurring counts
        jsonb_build_object(
        'recurring', COUNT(*) FILTER (WHERE issue.recurring_status = TRUE),
        'non_recurring', COUNT(*) FILTER (WHERE issue.recurring_status = FALSE)
        ) AS recurring_summary,

        -- Impact category counts
        (
        SELECT jsonb_object_agg(impact_category, count)
        FROM (
          SELECT issue.impact_category, COUNT(*) AS count
          FROM issue
          JOIN engagements ON issue.engagement = engagements.id
          JOIN annual_plans ON engagements.plan_id = annual_plans.id
          JOIN company_modules ON annual_plans.company_module = company_modules.id
          WHERE company_modules.id = %s
          GROUP BY issue.impact_category
        ) AS impact
        ) AS impact_summary,

        -- Issue status
        (
        SELECT jsonb_object_agg(status, count)
        FROM (
          SELECT issue.status, COUNT(*) AS count
          FROM issue
          JOIN engagements ON issue.engagement = engagements.id
          JOIN annual_plans ON engagements.plan_id = annual_plans.id
          JOIN company_modules ON annual_plans.company_module = company_modules.id
          WHERE company_modules.id = %s
          GROUP BY issue.status
        ) AS status
        ) AS status_summary,
  
        -- Business processes
        (
        SELECT jsonb_object_agg(process, count)
        FROM (
          SELECT issue.process, COUNT(*) AS count
          FROM issue
          JOIN engagements ON issue.engagement = engagements.id
          JOIN annual_plans ON engagements.plan_id = annual_plans.id
          JOIN company_modules ON annual_plans.company_module = company_modules.id
          WHERE company_modules.id = %s
          GROUP BY issue.process
          ORDER BY count DESC
          LIMIT 5
        ) AS process
        ) AS process_summary,

        -- Root cause
        (
        SELECT jsonb_object_agg(root_cause, count)
        FROM (
          SELECT issue.root_cause, COUNT(*) AS count
          FROM issue
          JOIN engagements ON issue.engagement = engagements.id
          JOIN annual_plans ON engagements.plan_id = annual_plans.id
          JOIN company_modules ON annual_plans.company_module = company_modules.id
          WHERE company_modules.id = %s
          GROUP BY issue.root_cause    
	    ) AS root_cause
        ) AS root_cause_summary
  
        FROM issue
        JOIN engagements ON issue.engagement = engagements.id
        JOIN annual_plans ON engagements.plan_id = annual_plans.id
        JOIN company_modules ON annual_plans.company_module = company_modules.id
        WHERE company_modules.id = %s;
        """
    )
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_module_id, company_module_id, company_module_id, company_module_id,company_module_id))
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
        COUNT(*) AS total_engagements,

        (
        SELECT jsonb_object_agg(status, count)
        FROM (
          SELECT status, COUNT(*) AS count
          FROM engagements
          WHERE plan_id = %s
          GROUP BY status
        ) AS status_counts
        ) AS status_summary

        FROM engagements
        WHERE plan_id = %s;
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

async def querying_engagement_details(connection: AsyncConnection, engagement_id: str):
    query = sql.SQL(
        """
        SELECT jsonb_build_object(
          'prepared', COUNT(*) FILTER (WHERE sub_program.prepared_by IS  NULL),
          'reviewed', COUNT(*) FILTER (WHERE sub_program.reviewed_by IS NULL),
            'completed', COUNT(*) FILTER (
              WHERE sub_program.prepared_by IS  NULL
                AND sub_program.reviewed_by IS  NULL
          )
        ) AS reviewer_summary
        FROM sub_program
        JOIN main_program ON sub_program.program = main_program.id
        JOIN engagements ON main_program.engagement = engagements.id
        WHERE engagements.id = %s;
        """
    )
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (engagement_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            audit_plan_data = [dict(zip(column_names, row_)) for row_ in rows]
            if audit_plan_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="Cant provide planning details check the module id")
            return audit_plan_data[0]

    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching planning details {e}")

