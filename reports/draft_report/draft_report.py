import os
import warnings
from docxtpl import DocxTemplate
from psycopg import AsyncConnection
from conv import converter
from reports.models.issue_model import load_engagement_report_data
from utils import exception_response

warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(BASE_DIR, "template.docx")
output_path = os.path.join(BASE_DIR, "final.docx")


async def generate_draft_report_model(
    engagement_id: str,
    module_id: str,
    connection: AsyncConnection,
):
    finding_path = os.path.join(BASE_DIR, f"{module_id}{engagement_id}-finding.docx")
    criteria_path = os.path.join(BASE_DIR, f"{module_id}{engagement_id}-criteria.docx")
    recommendation_path = os.path.join(BASE_DIR, f"{module_id}{engagement_id}-recommendation.docx")
    management_action_plan = os.path.join(BASE_DIR, f"{module_id}{engagement_id}-management_action_plan.docx")
    root_cause_description_path = os.path.join(BASE_DIR, f"{module_id}{engagement_id}-root_cause_description.docx")
    impact_description_path = os.path.join(BASE_DIR, f"{module_id}{engagement_id}-impact_description.docx")


    with exception_response():
        data = await load_engagement_report_data(
            connection=connection,
            engagement_id=engagement_id,
            module_id=module_id
        )

        doc = DocxTemplate(template_path)

        issues_context = []

        for da in data.issues:
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
                "root_cause_description": root_cause_description_sub_doc,
                "impact_category": da.impact_category,
                "impact_sub_category": da.impact_sub_category,
                "impact_description": impact_description_sub_doc,
                "finding": finding_sub_doc,
                "criteria": criteria_sub_doc,
                "recommendation": recommendation_sub_doc,
                "management_action_plan": management_action_plan_sub_doc,
                "responsible_people": da.responsible_people,
            })

        context = {
            "organization_name": data.organization_name,
            'engagement_code': data.engagement_code,
            "engagement_name": data.engagement_name,
            "issues": issues_context
        }

        doc.render(context)
        doc.save(output_path)
