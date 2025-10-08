import warnings
from reports.models.engagement_report_model import get_engagement_report_details
from reports.models.issue_report_model import issue_report_data_model
from reports.utils import create_styled_table
warnings.filterwarnings("ignore")
import os
from docx import Document
from docxtpl import DocxTemplate
from psycopg import AsyncConnection
from conv import converter
from utils import exception_response



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(BASE_DIR, "template.docx")
output_path = os.path.join(BASE_DIR, "final.docx")
table_of_content_path = os.path.join(BASE_DIR, "table_of_content.docx")


async def generate_finding_report(
    engagement_id: str,
    connection: AsyncConnection,
):
    with (exception_response()):
        finding_path = os.path.join(BASE_DIR, f"{engagement_id}-finding.docx")
        criteria_path = os.path.join(BASE_DIR, f"{engagement_id}-criteria.docx")
        recommendation_path = os.path.join(BASE_DIR, f"{engagement_id}-recommendation.docx")
        management_action_plan = os.path.join(BASE_DIR, f"{engagement_id}-management_action_plan.docx")
        root_cause_description_path = os.path.join(BASE_DIR, f"{engagement_id}-root_cause_description.docx")
        impact_description_path = os.path.join(BASE_DIR, f"{engagement_id}-impact_description.docx")

        engagement_data = await get_engagement_report_details(
            connection=connection,
            engagement_id=engagement_id
        )


        issue_data = await issue_report_data_model(
            connection=connection,
            engagement_id=engagement_id
        )


        doc = DocxTemplate(template_path)
        table_of_content = Document()
        table_of_content_headers = ["No", "Finding Title", "Finding Risk Rating"]


        table_of_content_data = []


        for index, issue in enumerate(issue_data, start=1):
            entry = [index, issue.title, issue.risk_rating]
            table_of_content_data.append(entry)


        create_styled_table(
            table_of_content,
            columns=3,
            headers=table_of_content_headers,
            data=table_of_content_data,
            column_widths=[0.1, 1.5, 2.5],
            header_bg="000094",          # dark blue header
            header_font_color="FFFFFF",  # white text
            row_bg="FFFFFF",             # light blue for data rows
            alt_row_bg="FFFFFF" ,         # white for alternating rows
            row_height=0.3
        )


        table_of_content.save(table_of_content_path)

        table_of_content_sub_doc = doc.new_subdoc(table_of_content_path)

        issues_context = []

        for da in issue_data:
            converter(filename=finding_path, data=da.finding)
            converter(filename=criteria_path, data=da.criteria)
            converter(filename=recommendation_path, data=da.recommendation)
            converter(filename=management_action_plan, data=da.management_action_plan)
            converter(filename=root_cause_description_path, data=da.root_cause_description)
            converter(filename=impact_description_path, data=da.impact_description)


            finding_sub_doc = doc.new_subdoc(finding_path)
            criteria_sub_doc = doc.new_subdoc(criteria_path)
            recommendation_sub_doc = doc.new_subdoc(recommendation_path)
            management_action_plan_sub_doc = doc.new_subdoc(management_action_plan)
            root_cause_description_sub_doc = doc.new_subdoc(root_cause_description_path)
            impact_description_sub_doc = doc.new_subdoc(impact_description_path)


            issues_context.append({
                "title": da.title,
                "process": da.process,
                "sub_process": da.sub_process,
                "risk_category": da.risk_category,
                "sub_risk_category": da.sub_risk_category,
                "recurring": "Yes" if da.recurring_status else "No",
                "rating": da.risk_rating,
                "root_cause": da.root_cause,
                "sub_root_cause": da.sub_root_cause,
                "root_cause_description": root_cause_description_sub_doc,
                "impact_category": da.impact_category,
                "impact_sub_category": da.impact_sub_category,
                "impact_description": impact_description_sub_doc,
                "finding": finding_sub_doc,
                "criteria": criteria_sub_doc,
                "recommendation": recommendation_sub_doc,
                "management_action_plan": management_action_plan_sub_doc,
                "responsible_people": da.responsible_people,
                "implementation_date": da.estimated_implementation_date.strftime("%d %b %Y")
            })


        context = {
            "organization_name": engagement_data.organization_name,
            'engagement_code': engagement_data.engagement_code,
            "engagement_name": engagement_data.engagement_name,
            "table1": table_of_content_sub_doc,
            "issues": issues_context
        }

        doc.render(context)
        doc.save(output_path)

        return output_path, engagement_data.engagement_name





