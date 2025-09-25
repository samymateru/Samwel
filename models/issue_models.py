from fastapi import HTTPException
from psycopg import AsyncConnection
from core.tables import Tables
from models.module_models import increment_module_reference
from schemas.issue_schemas import NewIssue, CreateIssue, IssueStatus, IssueColumns
from schemas.module_schemas import ModulesColumns, IncrementInternalIssues, IncrementExternalIssues
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from utils import exception_response, get_unique_key
from datetime import datetime

async def create_new_issue_model(
        connection: AsyncConnection,
        issue: NewIssue,
        module_id: str,
        engagement_id: str,
        sub_program_id: str
):
    with exception_response():
        __issue__ = CreateIssue(
            id=get_unique_key(),
            module_id=module_id,
            title=issue.title,
            ref=get_unique_key(),
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


async def generate_issue_reference(
        connection: AsyncConnection,
        module_id: str,
        source: str
):
    with exception_response():
        builder = (
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

            results = increment_module_reference(
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
            results = increment_module_reference(
                connection=connection,
                module_id=module_id,
                value=external_increment
            )
            if results is None:
                raise HTTPException(status_code=400, detail="Error Incrementing External Issue Reference")
            return reference
