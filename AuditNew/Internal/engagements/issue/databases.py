import json
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.issue.schemas import *
#from psycopg2 import IntegrityError, errors
#import psycopg2

def safe_json_dump(obj):
    return obj.model_dump_json() if obj is not None else '{}'

def edit_issue(connection: Connection, issue: Issue, issue_id: int):
    query = """
    UPDATE public.issue
    SET 
        title = %s,
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

def add_new_issue(connection: Connection, issue: Issue, sub_program_id: int, engagement_id: int):
    query: str = """
                    INSERT INTO public.issue (
                            sub_program,
                            engagement,
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
                            estimated_implementation_date,
                            regulatory,
                            status,
                            LOD1_implementer,
                            LOD1_owner,
                            LOD2_risk_manager,
                            LOD2_compliance_officer,
                            LOD3_audit_manager
                            ) VALUES (
                             %s, %s, %s, %s, %s, %s, %s,
                             %s, %s, %s, %s, %s, %s, %s, 
                             %s, %s, %s, %s, %s, %s,
                             %s, %s, %s, %s, %s, %s, %s
                            );

                 """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query,(
                sub_program_id,
                engagement_id,
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
                issue.estimated_implementation_date,
                issue.regulatory,
                issue.status,
                json.dumps(jsonable_encoder(issue.model_dump().get("LOD1_implementer"))),
                json.dumps(jsonable_encoder(issue.model_dump().get("LOD1_owner"))),
                json.dumps(jsonable_encoder(issue.model_dump().get("LOD2_risk_manager"))),
                json.dumps(jsonable_encoder(issue.model_dump().get("LOD2_compliance_officer"))),
                json.dumps(jsonable_encoder(issue.model_dump().get("LOD3_audit_manager")))
            ))
        connection.commit()
    # except psycopg2.IntegrityError as e:
    #     connection.rollback()
    #     if isinstance(e.__cause__, psycopg2.errors.ForeignKeyViolation):
    #         print("Foreign key violation: Parent record does not exist.")
    #     else:
    #         print("Some other integrity error:", e)
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
