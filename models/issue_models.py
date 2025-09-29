from typing import List

from fastapi import HTTPException
from psycopg import AsyncConnection
from core.tables import Tables
from models.module_models import increment_module_reference
from schemas.issue_schemas import NewIssue, CreateIssue, IssueStatus, IssueColumns, UpdateIssueStatus, NewIssueResponse, \
    CreateIssueResponses, IssueResponseColumns, UpdateIssueDetails, MarkIssueReportable, ReviseIssue
from schemas.module_schemas import ModulesColumns, IncrementInternalIssues, IncrementExternalIssues
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key
from datetime import datetime

async def create_new_issue_model(
        connection: AsyncConnection,
        issue: NewIssue,
        module_id: str,
        engagement_id: str,
        sub_program_id: str,
        reference: str
):
    with exception_response():
        __issue__ = CreateIssue(
            id=get_unique_key(),
            sub_program=sub_program_id,
            module_id=module_id,
            title=issue.title,
            ref=reference,
            criteria=issue.criteria,
            finding=issue.finding,
            source=issue.source,
            risk_rating=issue.risk_rating,
            created_at=datetime.now(),
            status=IssueStatus.NOT_STARTED,
            process=issue.process,
            sub_process=issue.sub_process,
            root_cause_description=issue.root_cause_description,
            root_cause=issue.root_cause,
            sub_root_cause=issue.sub_root_cause,
            impact_description=issue.impact_description,
            impact_category=issue.impact_category,
            impact_sub_category=issue.impact_sub_category,
            risk_category=issue.risk_category,
            sub_risk_category=issue.sub_risk_category,
            recommendation=issue.recommendation,
            management_action_plan=issue.management_action_plan,
            regulatory=issue.regulatory,
            estimated_implementation_date=issue.estimated_implementation_date,
            engagement=engagement_id
        )


        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ISSUES)
            .values(__issue__)
            .check_exists({IssueColumns.TITLE.value: issue.title})
            .check_exists({IssueColumns.SUB_PROGRAM.value: sub_program_id})
            .returning(IssueColumns.ID.value)
            .execute()
        )

        return builder



async def fetch_single_issue_item_model(
        connection: AsyncConnection,
        issue_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ISSUES)
            .where(IssueColumns.ID.value, issue_id)
            .fetch_one()
        )

        return builder



async def mark_issue_reportable_model(
        connection: AsyncConnection,
        issue_id: str
):
    with exception_response():
        __issue__ = MarkIssueReportable(
            reportable=True
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ISSUES.value)
            .values(__issue__)
            .check_exists({IssueColumns.ID.value: issue_id})
            .where({IssueColumns.ID.value: issue_id})
            .returning(IssueColumns.ID.value)
            .execute()
        )

        return builder



async def save_issue_responses(
        connection: AsyncConnection,
        response: NewIssueResponse,
        issue_id: str,
):
    with exception_response():
        __response__ = CreateIssueResponses(
            id=get_unique_key(),
            type=response.type,
            issued_by=response.issued_by,
            issue=issue_id,
            created_at=datetime.now(),
            notes=response.notes if response.notes is  not None else "",
            attachments=response.attachments
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ISSUE_RESPONSES.value)
            .values(__response__)
            .returning(IssueResponseColumns.ID.value)
            .execute()
        )
        return builder



async def revise_issue_model(
        connection: AsyncConnection,
        revised_date: datetime,
        issue_id: str,
):
    with exception_response():
        issue_data = await fetch_single_issue_item_model(
            connection=connection,
            issue_id=issue_id
        )

        count = int(issue_data.get("revised_count") or 0) + 1

        __revise__ = ReviseIssue(
            date_revised=revised_date,
            revised_status=True,
            revised_count=count
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ISSUES.value)
            .values(__revise__)
            .check_exists({IssueColumns.ID.value: issue_id})
            .where({IssueColumns.ID.value: issue_id})
            .returning(IssueColumns.ID.value)
            .execute()
        )

        return builder



async def generate_issue_reference(
        connection: AsyncConnection,
        module_id: str,
        source: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.MODULES.value)
            .where(ModulesColumns.ID.value, module_id)
            .fetch_one()
        )
        if builder is None:
            raise HTTPException(status_code=404, detail="Error While Generating Issue Reference, Module Not Found")

        if source == "Internal Audit":
            internal = builder.get("internal_issues") + 1
            reference = f"IA-{internal:05d}"

            internal_increment = IncrementInternalIssues(
                internal_issues=internal
            )

            results = await increment_module_reference(
                connection=connection,
                module_id=module_id,
                value=internal_increment
            )


            if results is None:
                raise HTTPException(status_code=400, detail="Error Incrementing Internal Issue Reference")
            return reference
        else:
            external = builder.get("external_issues") + 1
            reference = f"EA-{external:05d}"

            external_increment = IncrementExternalIssues(
                external_issues=external
            )
            results = await increment_module_reference(
                connection=connection,
                module_id=module_id,
                value=external_increment
            )

            if results is None:
                raise HTTPException(status_code=400, detail="Error Incrementing External Issue Reference")
            return reference



async def change_issue_status(
        connection: AsyncConnection,
        issue_id: str,
        issue_status: IssueStatus,
):
    with exception_response():
        __issue__ = UpdateIssueStatus(
            status=issue_status.value
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ISSUES.value)
            .values(__issue__)
            .check_exists({IssueColumns.ID.value: issue_id})
            .where({IssueColumns.ID.value: issue_id})
            .returning(IssueColumns.ID.value)
            .execute()
        )

        return builder



async def get_engagement_issues_model(
        connection: AsyncConnection,
        engagement_ids: List[str],
        module_id: str
):
    with exception_response():

        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ISSUES.value)
            .where(IssueColumns.ENGAGEMENT.value, engagement_ids)
            .where(IssueColumns.MODULE_ID.value, module_id)
            .fetch_all()
        )

        return builder





async def get_module_issues_model(
        connection: AsyncConnection,
        issue_id: str,
        issue_status: IssueStatus,
):
    with exception_response():
        pass



async def update_issue_details_model(
        connection: AsyncConnection,
        issue: UpdateIssueDetails,
        issue_id: str,
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ISSUES.value)
            .values(issue)
            .check_exists({IssueColumns.ID.value: issue_id})
            .where({IssueColumns.ID.value: issue_id})
            .returning(IssueColumns.ID.value)
            .execute()
        )

        return builder



async def delete_issue_details_model(
        connection: AsyncConnection,
        issue_id: str,
):
    with exception_response():

        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.ISSUES.value)
            .check_exists({IssueColumns.ID.value: issue_id})
            .where({IssueColumns.ID.value: issue_id})
            .returning(IssueColumns.ID.value)
            .execute()
        )

        return builder



async def issue_accept_model(
        connection: AsyncConnection,
        response: NewIssueResponse,
        status: IssueStatus,
        issue_id: str
):
    with exception_response():

        results = await change_issue_status(
            connection=connection,
            issue_id=issue_id,
            issue_status=status
        )

        if results is None:
            raise HTTPException(status_code=400, detail="Failed Accepting Issue")
