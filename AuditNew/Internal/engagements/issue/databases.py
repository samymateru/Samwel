import json
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from AuditNew.Internal.engagements.issue.schemas import *
from datetime import datetime
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

def send_issues_to_implementor(connection: Connection, issue_ids: IssueSendImplementation, user_email: str):
    try:
        issue_details = IssueImplementationDetails(
            notes="Issue sent to implementer",
            issued_by=User(
                name="",
                email=user_email,
                date_issued=datetime.now()
            ),
            type="send"
        )
        with connection.cursor() as cursor:
            placeholders = ','.join(['%s'] * len(issue_ids.model_dump().get("id")))
            query_issue: str = f"SELECT engagement FROM public.issue WHERE id IN ({placeholders})"
            cursor.execute(query_issue, issue_ids.id)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            issue_data = [dict(zip(column_names, row_)) for row_ in rows]
            for issue in issue_data:
                allowed_to_send_list = []
                cursor.execute("SELECT leads FROM public.engagements WHERE id = %s;", (issue.get("engagement"),))
                rows = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                leads = [dict(zip(column_names, row_)) for row_ in rows]
                for lead in leads[0].get("leads"):
                    allowed_to_send_list.append(lead.get("email"))
                if user_email in allowed_to_send_list:
                    data = get_issue_and_issue_actors(
                        connection=connection,
                        cursor=cursor,
                        issue_ids=issue_ids,
                        issue_actors=IssueActors.IMPLEMENTER,
                        status={IssueStatus.NOT_STARTED},
                        next_status=IssueStatus.OPEN,
                        issue_details=issue_details
                    )

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error send issues to implementor {e}")

def save_issue_implementation_(connection: Connection, issue_details: IssueImplementationDetails, issue_id: int, user_email: str):
    query_issue: str = """
                         SELECT * FROM public.issue WHERE id = %s;
                        """
    query_update: str = """
                         UPDATE public.issue
                         SET
                         status = %s
                         WHERE id = %s;
                        """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query_issue, (issue_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            issue_data = [dict(zip(column_names, row_)) for row_ in rows]
            allowed_to_save_list = []
            for implementer in issue_data[0].get(IssueActors.IMPLEMENTER.value):
                allowed_to_save_list.append(implementer.get("email"))
            if user_email in allowed_to_save_list:
                if issue_data[0].get("status") == IssueStatus.OPEN:
                    update_issue_details(
                        connection=connection,
                        cursor=cursor,
                        issue_details=issue_details,
                        issue_id=issue_id
                    )
                    cursor.execute(query_update, (IssueStatus.IN_PROGRESS_IMPLEMENTER, issue_id))
                    connection.commit()
                if issue_data[0].get("status") == IssueStatus.IN_PROGRESS_IMPLEMENTER:
                    update_issue_details(
                        connection=connection,
                        cursor=cursor,
                        issue_details=issue_details,
                        issue_id=issue_id
                    )
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error saving issue implementation {e}")

def send_issues_to_owner(connection: Connection, issue_id: int, user_email: str):
    query_issue: str = """
                         SELECT * FROM public.issue WHERE id = %s;
                        """
    try:
        issue_details = IssueImplementationDetails(
            notes="Issue sent to the owner",
            issued_by=User(
                name="",
                email=user_email,
                date_issued=datetime.now()
            ),
            type="send"
        )
        with connection.cursor() as cursor:
            cursor.execute(query_issue, (issue_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            issue_data = [dict(zip(column_names, row_)) for row_ in rows]
            allowed_to_save_list = []
            for implementer in issue_data[0].get(IssueActors.IMPLEMENTER.value):
                allowed_to_save_list.append(implementer.get("email"))
            if user_email in allowed_to_save_list:
                issue_ids = IssueSendImplementation(
                    id = [issue_id]
                )
                data = get_issue_and_issue_actors(
                    connection=connection,
                    cursor=cursor,
                    issue_ids=issue_ids,
                    issue_actors=IssueActors.OWNER,
                    status={IssueStatus.IN_PROGRESS_IMPLEMENTER},
                    next_status=IssueStatus.IN_PROGRESS_OWNER,
                    issue_details=issue_details
                )
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error sending issue to owner {e}")

def send_accept_response(connection: Connection, issue: IssueAcceptResponse, issue_id: int, user_email: str):
    query: str = """
                  SELECT * FROM public.issue WHERE id = %s
                 """
    issue_details = IssueImplementationDetails(
        notes=issue.accept_notes,
        attachment=issue.accept_attachment,
        issued_by=User(
            name="",
            email=user_email,
            date_issued=datetime.now()
        ),
        type="accept"
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (issue_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            issue_data = [dict(zip(column_names, row_)) for row_ in rows]
            allowed_actors_list = []
            for actor in issue_data[0].get(issue.actor.value):
                allowed_actors_list.append(actor.get("email"))
            if user_email in allowed_actors_list:
                issue_ids = IssueSendImplementation(
                    id=[issue_id]
                )
                match issue.actor:
                    case issue.actor.OWNER:
                        issue_actor = IssueActors.COMPLIANCE_OFFICER if issue_data[0].get("regulatory") else IssueActors.RISK_MANAGER
                        data = get_issue_and_issue_actors(
                            connection=connection,
                            cursor=cursor,
                            issue_ids=issue_ids,
                            issue_actors=issue_actor,
                            status={IssueStatus.IN_PROGRESS_OWNER},
                            next_status=IssueStatus.CLOSED_NOT_VERIFIED,
                            issue_details=issue_details
                        )
                    case issue.actor.RISK_MANAGER:
                        data = get_issue_and_issue_actors(
                            connection=connection,
                            cursor=cursor,
                            issue_ids=issue_ids,
                            issue_actors=IssueActors.AUDIT_MANAGER,
                            status={IssueStatus.CLOSED_NOT_VERIFIED},
                            next_status=str(issue.lod2_feedback.value),
                            issue_details=issue_details
                        )
                    case issue.actor.COMPLIANCE_OFFICER:
                        data = get_issue_and_issue_actors(
                            connection=connection,
                            cursor=cursor,
                            issue_ids=issue_ids,
                            issue_actors=IssueActors.AUDIT_MANAGER,
                            status={IssueStatus.CLOSED_NOT_VERIFIED},
                            next_status=str(issue.lod2_feedback.value),
                            issue_details=issue_details
                        )
                    case issue.actor.AUDIT_MANAGER:
                        data = []
                        update_issue_status(
                            connection=connection,
                            cursor=cursor,
                            issue_ids=issue_ids,
                            status=issue_data[0].get("status"),
                            next_status=IssueStatus.CLOSED_VERIFIED_BY_AUDIT
                        )
                    case _:
                        pass

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error sending accept response {e}")

def send_decline_response(connection: Connection, issue: IssueDeclineResponse, issue_id: int, user_email: str):
    query: str = """
                  SELECT * FROM public.issue WHERE id = %s
                 """
    try:
        issue_details = IssueImplementationDetails(
            notes=issue.decline_notes,
            issued_by=User(
                name="",
                email=user_email,
                date_issued=datetime.now()
            ),
            type="decline"
        )
        with connection.cursor() as cursor:
            cursor.execute(query, (issue_id,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            issue_data = [dict(zip(column_names, row_)) for row_ in rows]
            allowed_actors_list = []
            for actor in issue_data[0].get(issue.actor.value):
                allowed_actors_list.append(actor.get("email"))
            if user_email in allowed_actors_list:
                issue_ids = IssueSendImplementation(
                    id=[issue_id]
                )
                match issue.actor:
                    case issue.actor.AUDIT_MANAGER:
                        issue_actor = IssueActors.COMPLIANCE_OFFICER if issue_data[0].get("regulatory") else IssueActors.RISK_MANAGER
                        data = get_issue_and_issue_actors(
                            connection=connection,
                            cursor=cursor,
                            issue_ids=issue_ids,
                            issue_actors=issue_actor,
                            status={
                                IssueStatus.CLOSED_RISK_NA,
                                IssueStatus.CLOSED_RISK_ACCEPTED,
                                IssueStatus.CLOSED_VERIFIED_BY_RISK
                            },
                            next_status=IssueStatus.CLOSED_NOT_VERIFIED,
                            issue_details=issue_details
                        )

                    case issue.actor.RISK_MANAGER:
                        data = get_issue_and_issue_actors(
                            connection=connection,
                            cursor=cursor,
                            issue_ids=issue_ids,
                            issue_actors=IssueActors.OWNER,
                            status={IssueStatus.CLOSED_NOT_VERIFIED},
                            next_status=IssueStatus.IN_PROGRESS_OWNER,
                            issue_details=issue_details
                        )
                    case issue.actor.COMPLIANCE_OFFICER:
                        data = get_issue_and_issue_actors(
                            connection=connection,
                            cursor=cursor,
                            issue_ids=issue_ids,
                            issue_actors=IssueActors.OWNER,
                            status={IssueStatus.CLOSED_NOT_VERIFIED},
                            next_status=IssueStatus.IN_PROGRESS_OWNER,
                            issue_details=issue_details
                        )
                    case issue.actor.OWNER:
                        data = get_issue_and_issue_actors(
                            connection=connection,
                            cursor=cursor,
                            issue_ids=issue_ids,
                            issue_actors=IssueActors.IMPLEMENTER,
                            status={IssueStatus.IN_PROGRESS_OWNER},
                            next_status=IssueStatus.IN_PROGRESS_IMPLEMENTER,
                            issue_details=issue_details
                        )
                    case _:
                        pass
                print(data)

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error sending decline response {e}")

def get_issue_and_issue_actors(
        connection: Connection,
        cursor: Cursor,
        issue_ids: IssueSendImplementation,
        issue_actors: str,
        status: set[IssueStatus],
        next_status: str,
        issue_details: IssueImplementationDetails
):
    placeholders = ','.join(['%s'] * len(issue_ids.model_dump().get("id")))
    query_implementers: str= f"SELECT * FROM public.issue WHERE id IN ({placeholders})"
    query_update: str = f"""
        UPDATE public.issue
        SET status = %s
        WHERE id = %s;
    """
    cursor.execute(query_implementers, issue_ids.id)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    data = [dict(zip(column_names, row_)) for row_ in rows]
    issue_list = []
    for issue in data:
        implementors = []
        if issue.get("status") in status:
            for implementor in issue.get(issue_actors):
                implementors.append(implementor.get("email"))
            mailed_issue = MailedIssue(
                id=issue.get("id"),
                title=issue.get("title"),
                criteria=issue.get("criteria"),
                finding=issue.get("finding"),
                risk_rating=issue.get("risk_rating"),
                regulatory=issue.get("regulatory"),
                engagement=issue.get("engagement"),
                status=issue.get("status"),
                lod1_implementer=issue.get(IssueActors.IMPLEMENTER.value),
                lod1_owner=issue.get(IssueActors.OWNER.value),
                lod2_risk_manager=issue.get(IssueActors.RISK_MANAGER.value),
                lod2_compliance_officer=issue.get(IssueActors.COMPLIANCE_OFFICER.value),
                lod3_audit_manager=issue.get(IssueActors.AUDIT_MANAGER.value),
                implementors=implementors
            )
            if issue_details.type != "submit":
                update_issue_details(
                    connection=connection,
                    cursor=cursor,
                    issue_id=issue_ids.id[0],
                    issue_details=issue_details
                )
            issue_list.append(mailed_issue)
            cursor.execute(query_update, (next_status, issue.get("id")))

    connection.commit()
    return issue_list

def update_issue_status(cursor: Cursor, connection: Connection, issue_ids: IssueSendImplementation, status: str, next_status: str):
    status_ = {
        IssueStatus.CLOSED_RISK_NA,
        IssueStatus.CLOSED_RISK_ACCEPTED,
        IssueStatus.CLOSED_VERIFIED_BY_RISK
    }
    placeholders = ','.join(['%s'] * len(issue_ids.model_dump().get("id")))
    query = f"""
        UPDATE public.issue
        SET status = %s
        WHERE id IN ({placeholders})
    """
    if status in status_:
        params = [next_status] + issue_ids.id
        cursor.execute(query, params)
        connection.commit()

def get_issue_from_actor(connection: Connection, user_email: str):
    conditions = []
    params = []
    jsonb_columns = [
        IssueActors.IMPLEMENTER.value,
        IssueActors.OWNER.value,
        IssueActors.RISK_MANAGER.value,
        IssueActors.COMPLIANCE_OFFICER.value,
        IssueActors.AUDIT_MANAGER.value
    ]
    for col in jsonb_columns:
        conditions.append(f"""
            (
                status != 'Not started' AND EXISTS (
                    SELECT 1
                    FROM jsonb_array_elements(
                        CASE
                            WHEN {col} IS NOT NULL AND jsonb_typeof({col}) = 'array' THEN {col}
                            ELSE '[]'::jsonb
                        END
                    ) AS elem
                    WHERE elem->>%s = %s
                )
            )
        """)
        params.extend(["email", user_email])  # add key and value for each condition

    # Join all conditions with OR
    where_clause = " OR ".join(conditions)

    query = f"SELECT * FROM public.issue WHERE  {where_clause};"

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching issue by actors {e}")

def update_issue_details(connection: Connection, cursor: Cursor, issue_id: int, issue_details: IssueImplementationDetails):
    query: str = """
                  INSERT INTO public.implementation_details (issue, notes, attachments, issued_by, type)
                  VALUES (%s, %s, %s, %s, %s);
                 """
    cursor.execute(query, (
        issue_id,
        issue_details.notes,
        json.dumps(issue_details.model_dump().get("attachment")),
        issue_details.issued_by.model_dump_json(),
        issue_details.type
    ))
    connection.commit()




