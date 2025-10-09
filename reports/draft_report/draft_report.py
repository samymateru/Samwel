import os
import warnings

from docx import Document

from reports.models.process_summary_rating_model import process_summary_rating_model
from reports.utils import sanitize_for_xml, create_styled_table
from services.logging.logger import global_logger
from test import process_summary_page

warnings.filterwarnings("ignore")
from reports.models.engagement_report_model import get_engagement_report_details
from reports.models.issue_report_model import issue_report_data_model
from docxtpl import DocxTemplate
from psycopg import AsyncConnection
from conv import converter
from utils import exception_response



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(BASE_DIR, "template.docx")
output_path = os.path.join(BASE_DIR, "final.docx")
findings_table_path = os.path.join(BASE_DIR, "table_of_findings.docx")



async def generate_draft_report_model(
    engagement_id: str,
    connection: AsyncConnection,
):
    audit_background_path = os.path.join(BASE_DIR, f"{engagement_id}-audit_background.docx")
    key_legislations_path = os.path.join(BASE_DIR, f"{engagement_id}-key_legislations.docx")
    key_changes_path = os.path.join(BASE_DIR, f"{engagement_id}-key_changes.docx")
    system_path = os.path.join(BASE_DIR, f"{engagement_id}-system.docx")
    reliance_path = os.path.join(BASE_DIR, f"{engagement_id}-reliance.docx")
    process_summary_path = os.path.join(BASE_DIR, f"{engagement_id}-process_summary.docx")




    finding_path = os.path.join(BASE_DIR, f"{engagement_id}-finding.docx")
    criteria_path = os.path.join(BASE_DIR, f"{engagement_id}-criteria.docx")
    recommendation_path = os.path.join(BASE_DIR, f"{engagement_id}-recommendation.docx")
    management_action_plan = os.path.join(BASE_DIR, f"{engagement_id}-management_action_plan.docx")
    root_cause_description_path = os.path.join(BASE_DIR, f"{engagement_id}-root_cause_description.docx")
    impact_description_path = os.path.join(BASE_DIR, f"{engagement_id}-impact_description.docx")


    with exception_response():

        engagement_data = await get_engagement_report_details(
            connection=connection,
            engagement_id=engagement_id
        )

        issue_data = await issue_report_data_model(
            connection=connection,
            engagement_id=engagement_id
        )


        doc = DocxTemplate(template_path)

        converter(filename=audit_background_path, data=engagement_data.engagement_profile.audit_background or {})
        converter(filename=key_legislations_path, data=engagement_data.engagement_profile.key_legislations or {})
        converter(filename=key_changes_path, data=engagement_data.engagement_profile.key_changes or {})
        converter(filename=system_path, data=engagement_data.engagement_profile.relevant_systems or {})
        converter(filename=reliance_path, data=engagement_data.engagement_profile.reliance or {})


        audit_background_sub_doc = doc.new_subdoc(audit_background_path)
        key_legislations_sub_doc = doc.new_subdoc(key_legislations_path)
        key_changes_sub_doc = doc.new_subdoc(key_changes_path)
        system_sub_doc = doc.new_subdoc(system_path)
        reliance_sub_doc = doc.new_subdoc(reliance_path)

        issues_context = []


        table_of_findings = Document()
        table_of_findings_headers = ["No", "Matter Raised", "Finding Rating", "Department"]


        table_of_findings_data = []

        for index, issue in enumerate(issue_data, start=1):
            entry = [index, issue.title, issue.risk_rating, issue.process]
            table_of_findings_data.append(entry)


        create_styled_table(
            table_of_findings,
            columns=4,
            headers=table_of_findings_headers,
            data=table_of_findings_data,
            column_widths=[0, 2.5, 1.5, 1.5],
            header_bg="CEDEE5",          # dark blue header
            header_font_color="000000",  # white text
            row_bg="FFFFFF",             # light blue for data rows
            alt_row_bg="FFFFFF" ,         # white for alternating rows
            row_height=0.3
        )


        table_of_findings.save(findings_table_path)

        table_of_findings_sub_doc = doc.new_subdoc(findings_table_path)

        data = await process_summary_rating_model(
            connection=connection,
            engagement_id=engagement_id
        )

        process_summary_page(
            programs=data,
            filename=process_summary_path
        )


        for da in issue_data:
            converter(filename=finding_path, data=da.finding or {})
            converter(filename=criteria_path, data=da.criteria or {})
            converter(filename=recommendation_path, data=da.recommendation or {})
            converter(filename=management_action_plan, data=da.management_action_plan or {})
            converter(filename=root_cause_description_path, data=da.root_cause_description or {})
            converter(filename=impact_description_path, data=da.impact_description or {})


            finding_sub_doc = doc.new_subdoc(finding_path)
            criteria_sub_doc = doc.new_subdoc(criteria_path)
            recommendation_sub_doc = doc.new_subdoc(recommendation_path)
            management_action_plan_sub_doc = doc.new_subdoc(management_action_plan)
            root_cause_description_sub_doc = doc.new_subdoc(root_cause_description_path)
            impact_description_sub_doc = doc.new_subdoc(impact_description_path)
            process_summary_sub_doc = doc.new_subdoc(process_summary_path)


            # Append to context list
            issues_context.append({
                "title": sanitize_for_xml(da.title),
                "process": sanitize_for_xml(da.process),
                "sub_process": sanitize_for_xml(da.sub_process),
                "risk_category": sanitize_for_xml(da.risk_category),
                "sub_risk_category": sanitize_for_xml(da.sub_risk_category),
                "recurring": "Yes" if da.recurring_status else "No",
                "rating": sanitize_for_xml(da.risk_rating),
                "root_cause": sanitize_for_xml(da.root_cause),
                "sub_root_cause": sanitize_for_xml(da.sub_root_cause),
                "root_cause_description": root_cause_description_sub_doc,
                "impact_category": sanitize_for_xml(da.impact_category),
                "impact_sub_category": sanitize_for_xml(da.impact_sub_category),
                "impact_description": impact_description_sub_doc,
                "finding": finding_sub_doc,
                "criteria": criteria_sub_doc,
                "recommendation": recommendation_sub_doc,
                "management_action_plan": management_action_plan_sub_doc,
                "responsible_people": da.responsible_people,
                "implementation_date": da.estimated_implementation_date.strftime("%d %b %Y"),
            })

        temp_files = [
            audit_background_path,
            key_legislations_path,
            key_changes_path,
            system_path,
            reliance_path,
            finding_path,
            criteria_path,
            recommendation_path,
            management_action_plan,
            root_cause_description_path,
            impact_description_path,
            findings_table_path,
            process_summary_path
        ]



        context = {
            "organization_name": sanitize_for_xml(engagement_data.organization_name),
            "audit_background": audit_background_sub_doc,
            "key_legislations": key_legislations_sub_doc,
            "key_changes": key_changes_sub_doc,
            "relevant_systems": system_sub_doc,
            "reliance": reliance_sub_doc,
            'engagement_code': sanitize_for_xml(engagement_data.engagement_code),
            "engagement_name": sanitize_for_xml(engagement_data.engagement_name),
            "engagement_type": sanitize_for_xml(engagement_data.engagement_type),
            "engagement_opinion_rating": sanitize_for_xml(engagement_data.engagement_opinion_rating),
            "engagement_opinion_conclusion": sanitize_for_xml(engagement_data.engagement_opinion_conclusion),
            "credit_risk_rating": sanitize_for_xml(engagement_data.engagement_risk_maturity_rating.credit_risk.maturity_rating),
            "credit_risk_rationale": sanitize_for_xml(engagement_data.engagement_risk_maturity_rating.credit_risk.rating_rationale),
            "operational_risk_rating": sanitize_for_xml(engagement_data.engagement_risk_maturity_rating.operational_risk.maturity_rating),
            "operational_risk_rationale": sanitize_for_xml(engagement_data.engagement_risk_maturity_rating.operational_risk.rating_rationale),
            "strategic_risk_rating": sanitize_for_xml(engagement_data.engagement_risk_maturity_rating.strategic_risk.maturity_rating),
            "strategic_risk_rationale": sanitize_for_xml(engagement_data.engagement_risk_maturity_rating.strategic_risk.rating_rationale),
            "liquidity_risk_rating": sanitize_for_xml(engagement_data.engagement_risk_maturity_rating.liquidity_risk.maturity_rating),
            "liquidity_risk_rationale": sanitize_for_xml(engagement_data.engagement_risk_maturity_rating.liquidity_risk.rating_rationale),
            "compliance_risk_rating": sanitize_for_xml(engagement_data.engagement_risk_maturity_rating.compliance_risk.maturity_rating),
            "compliance_risk_rationale": sanitize_for_xml(engagement_data.engagement_risk_maturity_rating.compliance_risk.rating_rationale),
            "market_risk_rating": sanitize_for_xml(engagement_data.engagement_risk_maturity_rating.market_risk.maturity_rating),
            "market_risk_rationale": sanitize_for_xml(engagement_data.engagement_risk_maturity_rating.market_risk.rating_rationale),
            "overall_risk_rating": sanitize_for_xml(engagement_data.engagement_risk_maturity_rating.overall_risk_maturity_rating.maturity_rating),
            "overall_risk_rationale": sanitize_for_xml(engagement_data.engagement_risk_maturity_rating.overall_risk_maturity_rating.rating_rationale),
            "issues": issues_context,
            "findings_table": table_of_findings_sub_doc,
            "process_summary": process_summary_sub_doc
        }




        for f in temp_files:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except Exception as e:
                    global_logger(f"Could not delete {f}: {e}")


        doc.render(context)
        doc.save(output_path)

        return output_path, engagement_data.engagement_name
