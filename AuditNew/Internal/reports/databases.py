from fastapi import HTTPException
from psycopg import AsyncConnection, sql


async def get_main_reports(connection: AsyncConnection, company_module_id: str):
    query = sql.SQL(
        """
        SELECT 
        issue.id as issue_id,
        engagements.name AS engagement_name,
        engagements.code AS engagement_code,
        annual_plans.year as financial_year,
        engagements.opinion_rating as overall_opinion_rating,
        issue.title as issue_name,
        issue.risk_rating as issue_rating,
        issue.source as issue_source,
        issue.criteria as issue_criteria,
        issue.root_cause_description as root_cause_description,
        issue.impact_description as impact_description,
        issue.recommendation as issue_recommendation,
        issue.management_action_plan as issue_management_action_plan,
        issue.reportable as issue_reportable,
        CASE 
        WHEN issue.date_opened IS NOT NULL THEN 'Yes'
        ELSE 'No'
        END AS is_issue_sent_to_owner,
        issue.date_opened as date_issue_sent_to_client,
        issue.estimated_implementation_date as estimated_implementation_date,
        CASE 
        WHEN issue.revised_count IS NOT NULL AND issue.revised_count > 0 THEN 'Yes'
        ELSE 'No'
        END AS is_issue_revised,
        issue.date_revised as latest_revised_date,
        issue.date_closed as actual_implementation_date,
        issue.revised_count as issue_revised_count,
        CASE 
        WHEN (issue.date_revised::date - CURRENT_DATE) < 0 THEN 'Yes'
        ELSE 'No'
        END AS is_issue_pass_due,
        (issue.date_revised::date - CURRENT_DATE) AS days_remaining_to_implementation,
        CASE 
        WHEN (CURRENT_DATE - issue.date_revised::date) > 90 THEN 'Yes'
        ELSE 'No'
        END AS issue_due_more_than_90_days,
        CASE 
        WHEN (CURRENT_DATE - issue.date_revised::date) > 365 THEN 'Yes'
        ELSE 'No'
        END AS issue_due_more_than_365_days,
        issue.status as issue_overall_status,
        
        (
        SELECT STRING_AGG(CONCAT(elem->>'name', ' <', elem->>'email', '>'), ', ')
        FROM jsonb_array_elements(issue.lod1_owner) AS elem
        ) AS LOD1_owner,
        
        (
        SELECT STRING_AGG(CONCAT(elem->>'name', ' <', elem->>'email', '>'), ', ')
        FROM jsonb_array_elements(issue.lod1_implementer) AS elem
        ) AS LOD1_Implementer,
        
        (
        SELECT STRING_AGG(CONCAT(elem->>'name', ' <', elem->>'email', '>'), ', ')
        FROM jsonb_array_elements(issue.lod2_risk_manager) AS elem
        ) AS LOD2_Risk_Manager,
        
        (
        SELECT STRING_AGG(CONCAT(elem->>'name', ' <', elem->>'email', '>'), ', ')
        FROM jsonb_array_elements(issue.lod2_compliance_officer) AS elem
        ) AS LOD2_Compliance_Officer,
        
        (
        SELECT STRING_AGG(CONCAT(elem->>'name', ' <', elem->>'email', '>'), ', ')
        FROM jsonb_array_elements(issue.lod3_audit_manager) AS elem
        ) AS LOD3_Audit_Manager,
        
        (
        SELECT STRING_AGG(CONCAT(elem->>'name', ' <', elem->>'email', '>'), ', ')
        FROM jsonb_array_elements(issue.observers) AS elem
        ) AS Observers,
        
        issue.response as latest_response
        
        FROM issue
        JOIN engagements ON issue.engagement = engagements.id
        JOIN annual_plans ON engagements.plan_id = annual_plans.id
        JOIN company_modules ON annual_plans.company_module = company_modules.id
        WHERE company_modules.id = %s
        GROUP BY
        engagements.name,
        engagement_code,
        financial_year,
        overall_opinion_rating,
        issue_id,
        issue_name,
        issue_rating,
        issue_source,
        issue_criteria,
        root_cause_description,
        impact_description,
        issue_recommendation,
        management_action_plan,
        issue_reportable,
        date_issue_sent_to_client,
        estimated_implementation_date,
        issue_overall_status,
        LOD1_Owner,
        LOD1_Implementer,
        LOD2_Risk_Manager,
        LOD2_Compliance_Officer,
        LOD3_Audit_Manager,
        Observers,
        latest_revised_date,
        is_issue_revised,
        actual_implementation_date,
        issue_revised_count,
        days_remaining_to_implementation,
        issue_due_more_than_90_days,
        issue_due_more_than_365_days,
        is_issue_sent_to_owner,
        is_issue_pass_due,
        latest_response
        ;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_module_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            audit_plan_data = [dict(zip(column_names, row_)) for row_ in rows]
            if audit_plan_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="Cant provide issue details check the module id")
            return audit_plan_data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching issue details {e}")


async def get_summary_issue_reports(connection: AsyncConnection, company_module_id: str):
    query = sql.SQL(
        """
        SELECT 
        issue.id as issue_id,
        engagements.name AS engagement_name,
        engagements.code AS engagement_code,
        annual_plans.year as financial_year,
        engagements.opinion_rating as overall_opinion_rating,
        issue.title as issue_name,
        issue.risk_rating as issue_rating,
        issue.source as issue_source,
        issue.criteria as issue_criteria,
        issue.root_cause_description as root_cause_description,
        issue.impact_description as impact_description,
        issue.recommendation as issue_recommendation,
        issue.management_action_plan as issue_management_action_plan,
        issue.reportable as issue_reportable,
        CASE 
        WHEN issue.date_opened IS NOT NULL THEN 'Yes'
        ELSE 'No'
        END AS is_issue_sent_to_owner,
        issue.date_opened as date_issue_sent_to_client,
        issue.estimated_implementation_date as estimated_implementation_date,
        CASE 
        WHEN issue.revised_count IS NOT NULL AND issue.revised_count > 0 THEN 'Yes'
        ELSE 'No'
        END AS is_issue_revised,
        issue.date_revised as latest_revised_date,
        issue.date_closed as actual_implementation_date,
        issue.revised_count as issue_revised_count,
        CASE 
        WHEN (issue.date_revised::date - CURRENT_DATE) < 0 THEN 'Yes'
        ELSE 'No'
        END AS is_issue_pass_due,
        (issue.date_revised::date - CURRENT_DATE) AS days_remaining_to_implementation,
        CASE 
        WHEN (CURRENT_DATE - issue.date_revised::date) > 90 THEN 'Yes'
        ELSE 'No'
        END AS issue_due_more_than_90_days,
        CASE 
        WHEN (CURRENT_DATE - issue.date_revised::date) > 365 THEN 'Yes'
        ELSE 'No'
        END AS issue_due_more_than_365_days,
        issue.status as issue_overall_status,

        (
        SELECT STRING_AGG(CONCAT(elem->>'name', ' <', elem->>'email', '>'), ', ')
        FROM jsonb_array_elements(issue.lod1_owner) AS elem
        ) AS LOD1_owner,

        (
        SELECT STRING_AGG(CONCAT(elem->>'name', ' <', elem->>'email', '>'), ', ')
        FROM jsonb_array_elements(issue.lod1_implementer) AS elem
        ) AS LOD1_Implementer,

        (
        SELECT STRING_AGG(CONCAT(elem->>'name', ' <', elem->>'email', '>'), ', ')
        FROM jsonb_array_elements(issue.lod2_risk_manager) AS elem
        ) AS LOD2_Risk_Manager,

        (
        SELECT STRING_AGG(CONCAT(elem->>'name', ' <', elem->>'email', '>'), ', ')
        FROM jsonb_array_elements(issue.lod2_compliance_officer) AS elem
        ) AS LOD2_Compliance_Officer,

        (
        SELECT STRING_AGG(CONCAT(elem->>'name', ' <', elem->>'email', '>'), ', ')
        FROM jsonb_array_elements(issue.lod3_audit_manager) AS elem
        ) AS LOD3_Audit_Manager,

        (
        SELECT STRING_AGG(CONCAT(elem->>'name', ' <', elem->>'email', '>'), ', ')
        FROM jsonb_array_elements(issue.observers) AS elem
        ) AS Observers,

        issue.response as latest_response

        FROM issue
        JOIN engagements ON issue.engagement = engagements.id
        JOIN annual_plans ON engagements.plan_id = annual_plans.id
        JOIN company_modules ON annual_plans.company_module = company_modules.id
        WHERE company_modules.id = %s
        GROUP BY
        engagements.name,
        engagement_code,
        financial_year,
        overall_opinion_rating,
        issue_id,
        issue_name,
        issue_rating,
        issue_source,
        issue_criteria,
        root_cause_description,
        impact_description,
        issue_recommendation,
        management_action_plan,
        issue_reportable,
        date_issue_sent_to_client,
        estimated_implementation_date,
        issue_overall_status,
        LOD1_Owner,
        LOD1_Implementer,
        LOD2_Risk_Manager,
        LOD2_Compliance_Officer,
        LOD3_Audit_Manager,
        Observers,
        latest_revised_date,
        is_issue_revised,
        actual_implementation_date,
        issue_revised_count,
        days_remaining_to_implementation,
        issue_due_more_than_90_days,
        issue_due_more_than_365_days,
        is_issue_sent_to_owner,
        is_issue_pass_due,
        latest_response
        ;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (company_module_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            audit_plan_data = [dict(zip(column_names, row_)) for row_ in rows]
            if audit_plan_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="Cant provide issue details check the module id")
            return audit_plan_data
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching issue details {e}")