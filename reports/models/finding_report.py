from docx import Document
from docxtpl import DocxTemplate
from psycopg import AsyncConnection
from conv import converter
from reports.models.issue_finding_model import load_issue_finding, create_table_of_content
from utils import exception_response



async def generate_finding_report(
    engagement_id: str,
    module_id: str,
    connection: AsyncConnection,
):
    with exception_response():
        data = await load_issue_finding(
            connection=connection,
            engagement_id=engagement_id,
            module_id=module_id
        )

        doc = DocxTemplate("")
        docxs = Document()


        create_table_of_content(
            issues=data.issues,
            doc=docxs
        )

        docxs.save("table1.docx")

        table_of_content = doc.new_subdoc("table1.docx")

        issues_context = []

        for da in data.issues:
            converter(filename="finding.docx", data=da.finding)
            converter(filename="criteria.docx", data=da.criteria)
            converter(filename="recommendation.docx", data=da.recommendation)
            converter(filename="management_action_plan.docx", data=da.management_action_plan)
            converter(filename="root_cause_description.docx", data=da.root_cause_description)
            converter(filename="impact_description.docx", data=da.impact_description)

            finding_subdoc = doc.new_subdoc("finding.docx")
            criteria_subdoc = doc.new_subdoc("criteria.docx")
            recommendation_subdoc = doc.new_subdoc("recommendation.docx")
            management_action_plan_subdoc = doc.new_subdoc("management_action_plan.docx")
            root_cause_descrption_subdoc = doc.new_subdoc("root_cause_description.docx")
            impact_descrption_subdoc = doc.new_subdoc("impact_description.docx")

            # Append to context list
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
                "root_cause_description": root_cause_descrption_subdoc,
                "impact_category": da.impact_category,
                "impact_sub_category": da.impact_sub_category,
                "impact_description": impact_descrption_subdoc,
                "finding": finding_subdoc,
                "criteria": criteria_subdoc,
                "recommendation": recommendation_subdoc,
                "management_action_plan": management_action_plan_subdoc,
                "responsible_people": da.responsible_people,
            })

        context = {
            "organization_name": data.organization_name,
            'engagement_code': data.engagement_code,
            "engagement_name": data.engagement_name,
            "table1": table_of_content,
            "issues": issues_context
        }

        doc.render(context)
        doc.save("final_output.docx")





