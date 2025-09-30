from typing import List
from psycopg import AsyncConnection
from models.engagement_models import get_single_engagement_details
from models.issue_actor_models import get_all_issue_actors_on_issue_model
from models.issue_models import get_engagement_issues_model
from models.organization_models import get_module_organization
from reports.schemas.issue_finding_schema import ResponsiblePeople, IssuesFinding, IssueFindingSheet
from utils import exception_response
from docx import Document

async def load_issue_finding(
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

        issue_data = await get_engagement_issues_model(
            connection=connection,
            engagement_ids=[engagement_id],
            module_id=module_id
        )

        all_issues = []

        for issue in issue_data:
            user_details = await get_all_issue_actors_on_issue_model(
                connection=connection,
                issue_id=issue.get("id")
            )

            responsible_people = [ResponsiblePeople(**user) for user in user_details]
            issue["responsible_people"] = responsible_people
            all_issues.append(IssuesFinding(**issue))


        finding_data = IssueFindingSheet(
            organization_name=organization_data.get("name", ""),
            engagement_name=engagement_data.get("name", ""),
            engagement_code=engagement_data.get("code", ""),
            issues=all_issues
        )

        return finding_data


def create_table_of_content(issues, doc: Document):
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'No'
    hdr_cells[1].text = 'Tie'
    hdr_cells[2].text = 'Audit Finding Rating'

    for d in issues:
        row_cells = table.add_row().cells
        row_cells[1].text = d.get("title")
        row_cells[2].text = d.get("rating")




