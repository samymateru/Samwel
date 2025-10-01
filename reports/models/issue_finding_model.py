from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.opc.oxml import qn
from docx.oxml import OxmlElement
from docx.shared import RGBColor, Inches
from psycopg import AsyncConnection
from models.engagement_models import get_single_engagement_details
from models.issue_actor_models import get_all_issue_actors_on_issue_by_status_model
from models.issue_models import get_engagement_issues_model
from models.organization_models import get_module_organization
from reports.schemas.issue_finding_schema import ResponsiblePeople, IssuesFinding, IssueFindingSheet
from utils import exception_response
from docx import Document


from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background_color(cell, color_hex: str):
    """
    Set the background color of a table cell in a Word document.

    Args:
        cell: The cell object from a `docx` table.
        color_hex (str): Hex code like 'FF0000' (red), 'D9D9D9' (gray), etc.
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')     # <-- required
    shd.set(qn('w:color'), 'auto')    # <-- required
    shd.set(qn('w:fill'), color_hex)  # <-- actual background color

    # Remove existing <w:shd> if present (to avoid duplicates)
    for child in tcPr.findall(qn('w:shd')):
        tcPr.remove(child)

    tcPr.append(shd)



def set_cell_text_color(cell, color_hex: str):
    """
    Set the text color inside a cell.
    """
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.font.color.rgb = RGBColor.from_string(color_hex)





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
            user_details = await get_all_issue_actors_on_issue_by_status_model(
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
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'No'
    hdr_cells[1].text = 'Title'
    hdr_cells[2].text = 'Audit Finding Rating'

    for cell in hdr_cells:
        set_cell_text_color(cell, 'ffffff')
        set_cell_background_color(cell, '0000FF')  # Light grey




    for idx, d in enumerate(issues, start=1):
        row_cells = table.add_row().cells
        row_cells[0].text = str(idx)
        row_cells[1].text = d.title
        row_cells[2].text = d.risk_rating





