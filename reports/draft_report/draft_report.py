import os
import warnings
from io import BytesIO
warnings.filterwarnings("ignore")
from docx import Document
from docxtpl import DocxTemplate
from psycopg import AsyncConnection

from reports.models.process_summary_rating_model import process_summary_rating_model
from reports.models.engagement_report_model import get_engagement_report_details
from reports.models.issue_report_model import issue_report_data_model
from reports.utils import sanitize_for_xml, create_styled_table
from test import process_summary_page
from utils import exception_response
from conv import converter



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(BASE_DIR, "template.docx")
output_path = os.path.join(BASE_DIR, "final.docx")


async def generate_draft_report_model(engagement_id: str, connection: AsyncConnection):
    """Generate engagement report with all sections as in-memory subdocuments"""
    with exception_response():
        # Fetch engagement and issue data
        engagement_data = await get_engagement_report_details(connection, engagement_id)
        issue_data = await issue_report_data_model(connection, engagement_id)

        # Load main template
        doc = DocxTemplate(template_path)

        # Helper function to create subdoc from data
        def create_subdoc_from_data(data_dict):
            buffer = BytesIO()
            docx_obj = converter(filename=buffer, data=data_dict)  # Assuming your converter can accept file-like object
            buffer.seek(0)
            return doc.new_subdoc(buffer)

        audit_background_sub_doc = create_subdoc_from_data(engagement_data.engagement_profile.audit_background or {})
        key_legislations_sub_doc = create_subdoc_from_data(engagement_data.engagement_profile.key_legislations or {})
        key_changes_sub_doc = create_subdoc_from_data(engagement_data.engagement_profile.key_changes or {})
        system_sub_doc = create_subdoc_from_data(engagement_data.engagement_profile.relevant_systems or {})
        reliance_sub_doc = create_subdoc_from_data(engagement_data.engagement_profile.reliance or {})

        # Table of findings as in-memory DOCX
        table_of_findings = Document()
        table_of_findings_headers = ["No", "Matter Raised", "Finding Rating", "Department"]
        table_of_findings_data = [
            [idx + 1, issue.title, issue.risk_rating, issue.process]
            for idx, issue in enumerate(issue_data)
        ]
        create_styled_table(
            table_of_findings,
            columns=4,
            headers=table_of_findings_headers,
            data=table_of_findings_data,
            column_widths=[0, 2.5, 1.5, 1.5],
            header_bg="CEDEE5",
            header_font_color="000000",
            row_bg="FFFFFF",
            alt_row_bg="FFFFFF",
            row_height=0.3
        )
        findings_buffer = BytesIO()
        table_of_findings.save(findings_buffer)
        findings_buffer.seek(0)
        table_of_findings_sub_doc = doc.new_subdoc(findings_buffer)


        process_summary_data = await process_summary_rating_model(connection, engagement_id)
        process_summary_buffer = BytesIO()
        process_summary_page(programs=process_summary_data, filename_or_buffer=process_summary_buffer)
        process_summary_buffer.seek(0)
        process_summary_sub_doc = doc.new_subdoc(process_summary_buffer)


        issues_context = []
        for da in issue_data:
            finding_sub_doc = create_subdoc_from_data(da.finding or {})
            criteria_sub_doc = create_subdoc_from_data(da.criteria or {})
            recommendation_sub_doc = create_subdoc_from_data(da.recommendation or {})
            management_action_plan_sub_doc = create_subdoc_from_data(da.management_action_plan or {})
            root_cause_description_sub_doc = create_subdoc_from_data(da.root_cause_description or {})
            impact_description_sub_doc = create_subdoc_from_data(da.impact_description or {})

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

        # Build the final context for the template
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
            "issues": issues_context,
            "findings_table": table_of_findings_sub_doc,
            "process_summary": process_summary_sub_doc
        }

        # Render and save the final report
        doc.render(context)
        doc.save(output_path)

        return output_path, engagement_data.engagement_name
