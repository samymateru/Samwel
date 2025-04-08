import json
from typing import Dict, List
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.issue.schemas import *

def safe_json_dump(obj):
    return obj.model_dump_json() if obj is not None else '{}'

def edit_issue(connection: Connection, issue: Issue, issue_id: int):
    query = """
    UPDATE public.issue
    SET 
        title = %s,
        ref = %s,
        criteria = %s,
        finding = %s,
        risk_rating = %s,
        process = %s,
        sub_process = %s,
        root_cause_description = %s,
        root_cause = %s,
        sub_root_cause = %s,
        risk_category = %s,
        sub_risk_category = %s,
        impact_description = %s,
        impact_category = %s,
        impact_sub_category = %s,
        recurring_status = %s,
        recommendation = %s,
        management_action_plan = %s,
        estimated_implementation_date = %s
    WHERE id = %s;
    """
    values = (
        issue.title,
        issue.ref,
        issue.criteria,
        issue.finding,
        issue.risk_rating,
        issue.process,
        issue.sub_process,
        issue.root_cause_description,
        issue.root_cause,
        issue.sub_root_cause,
        issue.risk_category,
        issue.sub_risk_category,
        issue.impact_description,
        issue.impact_category,
        issue.impact_sub_category,
        issue.recurring_status,
        issue.recommendation,
        issue.management_action_plan,
        issue.estimated_implementation_date,
        issue_id
    )
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating issue {e}")

def add_new_issue(connection: Connection, issue: Issue, sub_program_id: int):
    query: str = """
                    INSERT INTO public.issue (
                            sub_program,
                            title,
                            criteria,
                            finding,
                            risk_rating,
                            process,
                            sub_process,
                            root_cause_description,
                            root_cause,
                            sub_root_cause,
                            risk_category,
                            sub_risk_category,
                            impact_description,
                            impact_category,
                            impact_sub_category,
                            recurring_status,
                            recommendation,
                            management_action_plan,
                            estimated_implementation_date
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);

                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(
                sub_program_id,
                issue.title,
                issue.criteria,
                issue.finding,
                issue.risk_rating,
                issue.process,
                issue.sub_process,
                issue.root_cause_description,
                issue.root_cause,
                issue.sub_root_cause,
                issue.risk_category,
                issue.sub_risk_category,
                issue.impact_description,
                issue.impact_category,
                issue.impact_sub_category,
                issue.recurring_status,
                issue.recommendation,
                issue.management_action_plan,
                issue.estimated_implementation_date
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating issue {e}")

def remove_issue(connection: Connection, issue_id: int):
    query: str = """
                  DELETE FROM public.issue WHERE id = %s
        
                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (issue_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting issue {e}")

def send_issue(connection: Connection, contacts: IssueContacts, issue_id: int):
    pass