from psycopg import AsyncConnection
from models.engagement_administration_profile_models import fetch_engagement_administration_profile_model
from models.engagement_models import get_single_engagement_details
from models.issue_actor_models import get_all_issue_actors_on_issue_by_status_model
from models.issue_models import get_engagement_issues_model
from models.organization_models import get_module_organization
from reports.schemas.issue_finding_schema import ResponsiblePeople, IssuesFinding, EngagementReport
from schemas.engagement_administration_profile_schemas import ReadEngagementAdministrationProfile
from utils import exception_response



async def load_engagement_report_data(
    connection: AsyncConnection,
    engagement_id: str,
    module_id: str
):
    with exception_response():
        organization_data = await get_module_organization(
            connection=connection,
            module_id=module_id
        )


        engagement_data = await get_single_engagement_details(
            connection=connection,
            engagement_id=engagement_id
        )

        engagement_profile_data = await fetch_engagement_administration_profile_model(
            connection=connection,
            engagement_id=engagement_id
        )


        issue_data = await get_engagement_issues_model(
            connection=connection,
            engagement_ids=[engagement_id],
            module_id=module_id
        )


        all_issues = []

        for issue in issue_data:
            user_details = await get_all_issue_actors_on_issue_by_status_model(
                connection=connection,
                issue_id=issue.get("id")
            )


            responsible_people = [ResponsiblePeople(**user) for user in user_details]
            issue["responsible_people"] = responsible_people
            all_issues.append(IssuesFinding(**issue))


        engagement_data = EngagementReport(
            organization_name=organization_data.get("name", ""),
            engagement_name=engagement_data.get("name", ""),
            engagement_profile=ReadEngagementAdministrationProfile(**engagement_profile_data),
            engagement_code=engagement_data.get("code", ""),
            issues=all_issues
        )

        return engagement_data