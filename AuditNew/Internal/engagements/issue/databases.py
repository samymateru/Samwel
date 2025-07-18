import json
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from AuditNew.Internal.engagements.issue.schemas import *
from datetime import datetime
from psycopg import AsyncConnection, AsyncCursor, sql
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from utils import get_unique_key

def safe_json_dump(obj):
    return obj.model_dump_json() if obj is not None else '{}'

async def edit_issue(connection: AsyncConnection, issue: Issue_, issue_id: str):
    query = sql.SQL(
    """
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
    """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (
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
                    ))
        await connection.commit()
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Issue already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating issue {e}")

async def add_new_issue(connection: AsyncConnection, issue: Issue_, sub_program_id: str, engagement_id: str):
    check_module_id_query = sql.SQL(
        """
        SELECT 
        cm.internal_issues AS internal,
        cm.external_issues AS external,
        cm.id
        FROM modules cm
        JOIN annual_plans ap ON ap.module = cm.id
        JOIN engagements e ON e.plan_id = ap.id
        WHERE e.id = {engagement_id};
        """).format(engagement_id=sql.Literal(engagement_id))

    update_company_module_internal = sql.SQL(
        """
        UPDATE public.modules 
        SET internal_issues = %s
        WHERE id = %s;
        """)

    update_company_module_external = sql.SQL(
        """
        UPDATE public.modules 
        SET external_issues = %s
        WHERE id = %s;
        """)

    query = sql.SQL(
        """
        INSERT INTO public.issue (
                id,
                ref,
                sub_program,
                engagement,
                title,
                criteria,
                finding,
                risk_rating,
                source,
                sdi_name,
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
                lod1_implementer,
                lod1_owner,
                observers,
                lod2_risk_manager,
                lod2_compliance_officer,
                lod3_audit_manager,
                date_revised,
                revised_count,
                reportable,
                revised_status,
                created_at
                )
        VALUES (
         %s, %s, %s, %s, %s, %s, %s, %s, %s,
         %s, %s, %s, %s, %s, %s, %s, %s, %s,
         %s, %s, %s, %s, %s, %s, %s, %s, %s,
         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(check_module_id_query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            reference = [dict(zip(column_names, row_)) for row_ in rows]
            if issue.source == "Internal Audit":
                pref = int(reference[0].get("internal")) + 1
                issue_id = f"IA-{pref:05d}"
                await cursor.execute(update_company_module_internal, (pref, reference[0].get("id")))
            else:
                pref = int(reference[0].get("external")) + 1
                issue_id = f"FND-{pref:05d}"
                await cursor.execute(update_company_module_external, (pref, reference[0].get("id")))

            await cursor.execute(query,(
                get_unique_key(),
                issue_id,
                sub_program_id,
                engagement_id,
                issue.title,
                issue.criteria,
                issue.finding,
                issue.risk_rating,
                issue.source,
                issue.sdi_name,
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
                json.dumps(jsonable_encoder(issue.model_dump().get(IssueActors.IMPLEMENTER.value))),
                json.dumps(jsonable_encoder(issue.model_dump().get(IssueActors.OWNER.value))),
                json.dumps(jsonable_encoder(issue.model_dump().get("observers"))),
                json.dumps(jsonable_encoder(issue.model_dump().get(IssueActors.RISK_MANAGER.value))),
                json.dumps(jsonable_encoder(issue.model_dump().get(IssueActors.COMPLIANCE_OFFICER.value))),
                json.dumps(jsonable_encoder(issue.model_dump().get(IssueActors.AUDIT_MANAGER.value))),
                issue.estimated_implementation_date,
                0,
                False,
                False,
                datetime.now()
            ))
        await connection.commit()
    except ForeignKeyViolation:
        await connection.rollback()
        raise HTTPException(status_code=400, detail="Sub program id is invalid")
    except UniqueViolation:
        await connection.rollback()
        raise HTTPException(status_code=409, detail="Issue already exist")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating issue {e}")

async def remove_issue(connection: AsyncConnection, issue_id: str):
    query = sql.SQL("DELETE FROM public.issue WHERE id = %s")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (issue_id,))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting issue {e}")

async def send_issues_to_implementor(connection: AsyncConnection, issue_ids: IssueSendImplementation, user_email: str):
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
        async with connection.cursor() as cursor:
            placeholders = sql.SQL(', ').join(sql.Placeholder() * len(issue_ids.model_dump().get("id")))
            query_issue = sql.SQL("SELECT engagement FROM public.issue WHERE id IN ({placeholders})").format(placeholders=placeholders)
            await cursor.execute(query_issue, issue_ids.id)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            issue_data = [dict(zip(column_names, row_)) for row_ in rows]
            if issue_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="Issue not found")
            for issue in issue_data:
                allowed_to_send_list = []
                await cursor.execute("SELECT leads FROM public.engagements WHERE id = %s;", (issue.get("engagement"),))
                rows = await cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                leads = [dict(zip(column_names, row_)) for row_ in rows]
                for lead in leads[0].get("leads"):
                    allowed_to_send_list.append(lead.get("email"))
                if user_email in allowed_to_send_list:
                    data = await get_issue_and_issue_actors(
                        connection=connection,
                        cursor=cursor,
                        issue_ids=issue_ids,
                        issue_actors=IssueActors.IMPLEMENTER,
                        status={IssueStatus.NOT_STARTED},
                        next_status=IssueStatus.OPEN,
                        issue_details=issue_details
                    )
                    query = sql.SQL(
                        """
                        UPDATE public.issue
                        SET date_opened = %s
                        WHERE id IN ({placeholders})
                        """).format(placeholders=placeholders)
                    params = [datetime.now()] + issue_ids.id
                    await cursor.execute(query, params)
                    await connection.commit()
                else:
                    raise HTTPException(status_code=403, detail="Your not team lead")
    except HTTPException as h:
        raise HTTPException(status_code=h.status_code, detail=h.detail)

    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error send issues to implementor {e}")

async def save_issue_implementation_(connection: AsyncConnection, issue_details: IssueImplementationDetails, issue_id: str, user_email: str):
    query_issue = sql.SQL("SELECT * FROM public.issue WHERE id = %s;")
    query_update = sql.SQL(
        """
         UPDATE public.issue
         SET
         status = %s,
         response = %s
         WHERE id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query_issue, (issue_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            issue_data = [dict(zip(column_names, row_)) for row_ in rows]
            allowed_to_save_list = []
            if issue_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="Issue not found")
            for implementer in issue_data[0].get(IssueActors.IMPLEMENTER.value):
                allowed_to_save_list.append(implementer.get("email"))
            if user_email in allowed_to_save_list:
                if issue_data[0].get("status") == IssueStatus.OPEN.value or IssueStatus.IN_PROGRESS_IMPLEMENTER.value:
                    await update_issue_details(
                        connection=connection,
                        cursor=cursor,
                        issue_details=issue_details,
                        issue_id=issue_id
                    )
                    await cursor.execute(query_update, (
                        IssueStatus.IN_PROGRESS_IMPLEMENTER,
                        issue_details.notes,
                        issue_id))
                    await connection.commit()
                return True
            else:
                raise HTTPException(status_code=403, detail="Your not issue implementer")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error saving issue implementation {e}")

async def send_issues_to_owner(connection: AsyncConnection, issue_id: str, user_email: str, user_name: str):
    query_issue = sql.SQL("SELECT * FROM public.issue WHERE id = %s;")
    try:
        issue_details = IssueImplementationDetails(
            notes="Issue sent to the owner",
            issued_by=User(
                name=user_name,
                email=user_email,
                date_issued=datetime.now()
            ),
            type="send"
        )
        async with connection.cursor() as cursor:
            await cursor.execute(query_issue, (issue_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            issue_data = [dict(zip(column_names, row_)) for row_ in rows]
            allowed_to_save_list = []
            if issue_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="Issue not found")
            for implementer in issue_data[0].get(IssueActors.IMPLEMENTER.value):
                allowed_to_save_list.append(implementer.get("email"))
            if user_email in allowed_to_save_list:
                issue_ids = IssueSendImplementation(
                    id = [issue_id]
                )
                data = await get_issue_and_issue_actors(
                    connection=connection,
                    cursor=cursor,
                    issue_ids=issue_ids,
                    issue_actors=IssueActors.OWNER,
                    status={IssueStatus.IN_PROGRESS_IMPLEMENTER},
                    next_status=IssueStatus.IN_PROGRESS_OWNER,
                    issue_details=issue_details
                )
                return True
            else:
                raise HTTPException(status_code=403, detail="Your not issue implementer")
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error sending issue to owner {e}")

async def send_accept_response(connection: AsyncConnection, issue: IssueAcceptResponse, issue_id: str, user_email: str, user_name: str):
    query = sql.SQL("SELECT * FROM public.issue WHERE id = %s")
    issue_details = IssueImplementationDetails(
        notes=issue.accept_notes,
        attachments=issue.accept_attachment,
        issued_by=User(
            name=user_name,
            email=user_email,
            date_issued=datetime.now()
        ),
        type="accept"
    )
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (issue_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            issue_data = [dict(zip(column_names, row_)) for row_ in rows]
            allowed_actors_list = []
            if issue_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="Issue not found")
            for actor in issue_data[0].get(issue.actor.value):
                allowed_actors_list.append(actor.get("email"))
            if user_email in allowed_actors_list:
                issue_ids = IssueSendImplementation(
                    id=[issue_id]
                )
                match issue.actor:
                    case issue.actor.OWNER:
                        issue_actor = IssueActors.COMPLIANCE_OFFICER if issue_data[0].get("regulatory") else IssueActors.RISK_MANAGER
                        data = await get_issue_and_issue_actors(
                            connection=connection,
                            cursor=cursor,
                            issue_ids=issue_ids,
                            issue_actors=issue_actor,
                            status={IssueStatus.IN_PROGRESS_OWNER},
                            next_status=IssueStatus.CLOSED_NOT_VERIFIED,
                            issue_details=issue_details
                        )
                    case issue.actor.RISK_MANAGER:
                        if issue_data[0].get("revised_status"):
                            data = await get_issue_and_issue_actors(
                                connection=connection,
                                cursor=cursor,
                                issue_ids=issue_ids,
                                issue_actors=IssueActors.IMPLEMENTER,
                                status={IssueStatus.CLOSED_NOT_VERIFIED},
                                next_status=IssueStatus.IN_PROGRESS_IMPLEMENTER,
                                issue_details=issue_details
                            )
                            update = sql.SQL("""
                                            UPDATE public.issue SET 
                                            revised_status = %s,
                                            response = %s
                                            WHERE id = %s
                                            """)
                            await cursor.execute(update, (
                                False,
                                issue_details.notes,
                                issue_id
                            ))
                            await connection.commit()
                        else:
                            data = await get_issue_and_issue_actors(
                                connection=connection,
                                cursor=cursor,
                                issue_ids=issue_ids,
                                issue_actors=IssueActors.AUDIT_MANAGER,
                                status={IssueStatus.CLOSED_NOT_VERIFIED},
                                next_status=str(issue.lod2_feedback.value),
                                issue_details=issue_details
                            )

                    case issue.actor.COMPLIANCE_OFFICER:
                        if issue_data[0].get("revised_status"):
                            data = await get_issue_and_issue_actors(
                                connection=connection,
                                cursor=cursor,
                                issue_ids=issue_ids,
                                issue_actors=IssueActors.IMPLEMENTER,
                                status={IssueStatus.CLOSED_NOT_VERIFIED},
                                next_status=IssueStatus.IN_PROGRESS_IMPLEMENTER,
                                issue_details=issue_details
                            )
                            update = sql.SQL("""
                                        UPDATE public.issue SET 
                                        revised_status = %s,
                                        response = %s
                                        WHERE id = %s
                                        """)
                            await cursor.execute(update, (
                                False,
                                issue_details.notes,
                                issue_id
                            ))
                            await connection.commit()
                        else:
                            data = await get_issue_and_issue_actors(
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
                        query_ = sql.SQL(
                            """
                            UPDATE public.issue
                            SET 
                            date_closed = %s,
                            response = %s
                            WHERE id = %s
                            """)
                        await cursor.execute(query_, (datetime.now(), issue.accept_notes, issue_id))
                        await connection.commit()
                        await update_issue_status(
                            connection=connection,
                            cursor=cursor,
                            issue_ids=issue_ids,
                            status=issue_data[0].get("status"),
                            next_status=IssueStatus.CLOSED_VERIFIED_BY_AUDIT
                        )
                        await update_issue_details(
                            connection=connection,
                            cursor=cursor,
                            issue_id=issue_id,
                            issue_details=issue_details
                        )
                    case _:
                        pass
                return True
            else:
                raise HTTPException(status_code=403, detail=f"Your not issue {issue.actor.value}")

    except HTTPException:
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error sending accept response {e}")

async def send_decline_response(connection: AsyncConnection, issue: IssueDeclineResponse, issue_id: str, user_email: str, user_name: str):
    query = sql.SQL("SELECT * FROM public.issue WHERE id = %s")
    try:
        issue_details = IssueImplementationDetails(
            notes=issue.decline_notes,
            issued_by=User(
                name=user_name,
                email=user_email,
                date_issued=datetime.now()
            ),
            type="decline"
        )
        async with connection.cursor() as cursor:
            await cursor.execute(query, (issue_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            issue_data = [dict(zip(column_names, row_)) for row_ in rows]
            allowed_actors_list = []
            if issue_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="Issue not found")
            for actor in issue_data[0].get(issue.actor.value):
                allowed_actors_list.append(actor.get("email"))
            if user_email in allowed_actors_list:
                issue_ids = IssueSendImplementation(
                    id=[issue_id]
                )
                match issue.actor:
                    case issue.actor.AUDIT_MANAGER:
                        issue_actor = IssueActors.COMPLIANCE_OFFICER if issue_data[0].get("regulatory") else IssueActors.RISK_MANAGER
                        data = await get_issue_and_issue_actors(
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
                        data = await get_issue_and_issue_actors(
                            connection=connection,
                            cursor=cursor,
                            issue_ids=issue_ids,
                            issue_actors=IssueActors.OWNER,
                            status={IssueStatus.CLOSED_NOT_VERIFIED},
                            next_status=IssueStatus.IN_PROGRESS_OWNER,
                            issue_details=issue_details
                        )
                    case issue.actor.COMPLIANCE_OFFICER:
                        data = await get_issue_and_issue_actors(
                            connection=connection,
                            cursor=cursor,
                            issue_ids=issue_ids,
                            issue_actors=IssueActors.OWNER,
                            status={IssueStatus.CLOSED_NOT_VERIFIED},
                            next_status=IssueStatus.IN_PROGRESS_OWNER,
                            issue_details=issue_details
                        )
                    case issue.actor.OWNER:
                        data = await get_issue_and_issue_actors(
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
                return True
            else:
                raise HTTPException(status_code=403, detail=f"Your not issue {issue.actor.value}")
    except HTTPException:
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error sending decline response {e}")

async def get_issue_and_issue_actors(
        connection: AsyncConnection,
        cursor: AsyncCursor,
        issue_ids: IssueSendImplementation,
        issue_actors: str,
        status: set[IssueStatus],
        next_status: str,
        issue_details: IssueImplementationDetails
):
    placeholders = sql.SQL(', ').join(sql.Placeholder() * len(issue_ids.model_dump().get("id")))
    query_implementers = sql.SQL("SELECT * FROM public.issue WHERE id IN ({placeholders})").format(placeholders=placeholders)
    query_update = sql.SQL(
        """
        UPDATE public.issue
        SET 
        status = %s,
        response = %s
        WHERE id = %s;
        """)
    await cursor.execute(query_implementers, issue_ids.id)
    rows = await cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    data = [dict(zip(column_names, row_)) for row_ in rows]
    issue_list = []
    for issue in data:
        implementors = []
        if issue.get("status") in status:
            for implementor in issue.get(issue_actors) or []:
                email = implementor.get("email")
                if email:
                    implementors.append(email)
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
            await update_issue_details(
                connection=connection,
                cursor=cursor,
                issue_id=issue_ids.id[0],
                issue_details=issue_details
            )
            issue_list.append(mailed_issue)
            await cursor.execute(query_update, (next_status, issue_details.notes, issue.get("id")))
            await connection.commit()
        else:
            raise HTTPException(status_code=403, detail="Issue cant be updated right now")
    return issue_list

async def update_issue_status(cursor: AsyncCursor, connection: AsyncConnection, issue_ids: IssueSendImplementation, status: str, next_status: str):
    status_ = {
        IssueStatus.CLOSED_RISK_NA,
        IssueStatus.CLOSED_RISK_ACCEPTED,
        IssueStatus.CLOSED_VERIFIED_BY_RISK
    }
    placeholders = sql.SQL(', ').join(sql.Placeholder() * len(issue_ids.model_dump().get("id")))
    query = sql.SQL(
        """
        UPDATE public.issue
        SET status = %s
        WHERE id IN ({placeholders})
        """).format(placeholders=placeholders)
    if status in status_:
        params = [next_status] + issue_ids.id
        await cursor.execute(query, params)
        await connection.commit()
    else:
        raise HTTPException(status_code=403, detail="Issue cant be updated right now")

async def get_issue_from_actor(connection: AsyncConnection, user_email: str):
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
        conditions.append(sql.SQL("""
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
        """).format(col=sql.Identifier(col)))
        params.extend(["email", user_email])  # add key and value for each condition

    # Join all conditions with OR
    where_clause = sql.SQL(" OR ").join(conditions)

    query = sql.SQL("SELECT * FROM public.issue WHERE  {where_clause};").format(where_clause=where_clause)

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, params)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching issue by actors {e}")

async def get_single_issue(connection: AsyncConnection, issue_id: str):
    query = sql.SQL("SELECT * FROM public.issue WHERE  id = %s")

    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (issue_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching single issue {e}")

async def update_issue_details(connection: AsyncConnection, cursor: AsyncCursor, issue_id: str, issue_details: IssueImplementationDetails):
    query = sql.SQL(
        """
          INSERT INTO public.implementation_details (id, issue, notes, attachments, issued_by, type)
          VALUES (%s, %s, %s, %s, %s, %s);
        """)
    await cursor.execute(query, (
        get_unique_key(),
        issue_id,
        issue_details.notes,
        json.dumps(issue_details.model_dump().get("attachments")),
        issue_details.issued_by.model_dump_json(),
        issue_details.type
    ))
    await connection.commit()

async def get_issue_updates(connection: AsyncConnection, issue_id: str):
    query = sql.SQL("SELECT * FROM public.implementation_details WHERE issue = %s;")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (issue_id,))
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error fetching issue details {e}")

async def mark_issue_prepared(connection: AsyncConnection, prepare: User, issue_id: str):
    query = sql.SQL(
        """
          UPDATE public.issue
          SET 
          prepared_by = %s::jsonb
          WHERE id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (prepare.model_dump_json(), issue_id))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error mark issue prepared {e}")

async def mark_issue_reviewed(connection: AsyncConnection, review: User, issue_id: str):
    query = sql.SQL(
        """
          UPDATE public.issue
          SET 
          reviewed_by = %s::jsonb
          WHERE id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (review.model_dump_json(), issue_id))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error mark issue reviewed {e}")

async def mark_issue_reportable(connection: AsyncConnection, reportable: bool, issue_id: str):
    query = sql.SQL(
        """
          UPDATE public.issue
          SET 
          reportable = %s
          WHERE id = %s;
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query, (reportable, issue_id))
        await connection.commit()
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error mark issue reportable {e}")

async def request_extension_time(connection: AsyncConnection, revise: Revise, issue_id: str, issue_details: IssueImplementationDetails, user_email: str):
    query = sql.SQL(
        """
        SELECT revised_count, lod1_implementer FROM public.issue WHERE id = {issue_id}
        """).format(issue_id=sql.Literal(issue_id))

    query_update_revise = sql.SQL(
        """
        UPDATE public.issue
        SET
        date_revised = %s,
        revised_count = %s,
        response = %s,
        revised_status = %s,
        status = %s
        WHERE id = %s
        """)
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            issue_data = [dict(zip(column_names, row_)) for row_ in rows]
            allowed_to_save_list = []
            if issue_data.__len__() == 0:
                raise HTTPException(status_code=400, detail="Issue not found")
            for implementer in issue_data[0].get(IssueActors.IMPLEMENTER.value):
                allowed_to_save_list.append(implementer.get("email"))
            if user_email in allowed_to_save_list:
                await cursor.execute(query_update_revise, (
                    revise.revised_date,
                    int(issue_data[0].get("revised_count")) + 1,
                    revise.reason,
                    True,
                    IssueStatus.IN_PROGRESS_OWNER.value,
                    issue_id
                ))
                await connection.commit()
                await update_issue_details(
                    connection=connection,
                    cursor=cursor,
                    issue_id=issue_id,
                    issue_details=issue_details
                )
            else:
                raise HTTPException(status_code=403, detail=f"Your not Implementor")
    except HTTPException:
        raise
    except Exception as e:
        await connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error request extension time {e}")


