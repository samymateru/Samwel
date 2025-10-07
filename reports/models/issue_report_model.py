from psycopg import AsyncConnection
from core.tables import Tables
from models.issue_actor_models import get_all_issue_actors_on_issue_by_status_model
from reports.schemas.issue_finding_schema import ResponsiblePeople, IssuesFinding
from schemas.issue_schemas import IssueColumns
from services.connections.postgres.read import ReadBuilder
from utils import exception_response


async def engagement_report_data_model(
    connection: AsyncConnection,
    engagement_id: str,
):
    with exception_response():

        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ISSUES.value)
            .where(IssueColumns.ENGAGEMENT.value, engagement_id)
            .fetch_all()
        )


        issues = []

        for issue in builder:
            user_details = await get_all_issue_actors_on_issue_by_status_model(
                connection=connection,
                issue_id=issue.get("id")
            )

            responsible_people = [ResponsiblePeople(**user) for user in user_details]
            issue["responsible_people"] = responsible_people
            issues.append(IssuesFinding(**issue))

        return issues




