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

def send_issues_to_implementor(connection: Connection, issue_ids: IssueSendImplementation):
    try:
        with connection.cursor() as cursor:
            data = get_issue_and_issue_actors(
                cursor=cursor,
                issue_ids=issue_ids,
                issue_actors=IssueActors.IMPLEMENTER)

            update_issue_status(
                cursor=cursor,
                connection=connection,
                issue_ids=issue_ids,
                status=IssueStatus.OPEN)
            print(data)
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error send issues to implementor {e}")

def send_issues_to_owner(connection: Connection, issue_id: int):

    try:
        with connection.cursor() as cursor:
            issue_ids = IssueSendImplementation(
                id = [issue_id]
            )
            data = get_issue_and_issue_actors(
                cursor=cursor,
                issue_ids=issue_ids,
                issue_actors=IssueActors.OWNER
            )
            update_issue_status(
                cursor=cursor,
                connection=connection,
                issue_ids=issue_ids,
                status=IssueStatus.IN_PROGRESS_OWNER
            )
            print(data)
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error sending issue to owner {e}")

def send_accept_response(connection: Connection, issue: IssueAcceptResponse, issue_id: int):
    query: str = """
                  SELECT regulatory FROM public.issue WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (issue_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            match issue.actor:
                case issue.actor.OWNER:
                    issue_actor = IssueActors.COMPLIANCE_OFFICER if data[0].get("regulatory") else IssueActors.RISK_MANAGER
                    issue_status = IssueStatus.CLOSED_NOT_VERIFIED
                case issue.actor.RISK_MANAGER:
                    issue_actor = IssueActors.AUDIT_MANAGER
                    issue_status = issue.lod2_feedback.value
                case issue.actor.COMPLIANCE_OFFICER:
                    issue_actor = IssueActors.AUDIT_MANAGER
                    issue_status = issue.lod2_feedback.value
                case issue.actor.AUDIT_MANAGER:
                    issue_actor = IssueActors.AUDIT_MANAGER
                    issue_status = IssueStatus.CLOSED_VERIFIED_BY_AUDIT
                case _:
                    pass
            issue_ids = IssueSendImplementation(
                id=[issue_id]
            )
            if issue.actor.value == issue.actor.AUDIT_MANAGER:
                update_issue_status(
                    cursor=cursor,
                    connection=connection,
                    issue_ids=issue_ids,
                    status=issue_status
                )
            else:
                data = get_issue_and_issue_actors(
                    cursor=cursor,
                    issue_ids=issue_ids,
                    issue_actors=issue_actor
                )

                update_issue_status(
                    cursor=cursor,
                    connection=connection,
                    issue_ids=issue_ids,
                    status=issue_status
                )

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error sending accept response {e}")

def send_decline_response(connection: Connection, issue: IssueDeclineResponse, issue_id: int):
    query: str = """
                  SELECT regulatory FROM public.issue WHERE id = %s
                 """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (issue_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = [dict(zip(column_names, row_)) for row_ in rows]
            match issue.actor:
                case issue.actor.AUDIT_MANAGER:
                    issue_actor = IssueActors.COMPLIANCE_OFFICER if data[0].get("regulatory") else IssueActors.RISK_MANAGER
                    issue_status = IssueStatus.CLOSED_NOT_VERIFIED
                case issue.actor.RISK_MANAGER:
                    issue_actor = IssueActors.OWNER
                    issue_status = IssueStatus.IN_PROGRESS_IMPLEMENTER
                case issue.actor.COMPLIANCE_OFFICER:
                    issue_actor = IssueActors.OWNER
                    issue_status = IssueStatus.IN_PROGRESS_IMPLEMENTER
                case issue.actor.OWNER:
                    issue_actor = IssueActors.IMPLEMENTER
                    issue_status = IssueStatus.OPEN
                case issue.actor.IMPLEMENTER:
                    issue_actor = IssueActors.IMPLEMENTER
                    issue_status = IssueStatus.OPEN

            issue_ids = IssueSendImplementation(
                id=[issue_id]
            )
            if issue.actor is not IssueActors.IMPLEMENTER:
                data = get_issue_and_issue_actors(
                    cursor=cursor,
                    issue_ids=issue_ids,
                    issue_actors=issue_actor
                )

                update_issue_status(
                    cursor=cursor,
                    connection=connection,
                    issue_ids=issue_ids,
                    status=issue_status
                )

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error sending decline response {e}")


def get_issue_and_issue_actors(cursor: Cursor, issue_ids: IssueSendImplementation, issue_actors: str):
    placeholders = ','.join(['%s'] * len(issue_ids.model_dump().get("id")))
    query_implementers: str= f"SELECT * FROM public.issue WHERE id IN ({placeholders})"
    cursor.execute(query_implementers, issue_ids.id)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    data = [dict(zip(column_names, row_)) for row_ in rows]
    issue_list = []
    for issue in data:
        implementors = []
        for implementor in issue.get(issue_actors):
            implementors.append(implementor.get("email"))
        mailed_issue = MailedIssue(
            title=issue.get("title"),
            criteria=issue.get("criteria"),
            finding=issue.get("finding"),
            risk_rating=issue.get("risk_rating"),
            implementors=implementors
        )
        issue_list.append(mailed_issue)
    return issue_list

def update_issue_status(cursor: Cursor, connection: Connection, issue_ids: IssueSendImplementation, status: str):
    placeholders = ','.join(['%s'] * len(issue_ids.model_dump().get("id")))
    query = f"""
        UPDATE public.issue
        SET status = %s
        WHERE id IN ({placeholders})
    """
    params = [status] + issue_ids.id
    cursor.execute(query, params)
    connection.commit()