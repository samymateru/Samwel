import warnings

from docx import Document

from reports.models.engagement_report_model import get_engagement_report_details
from reports.utils import create_styled_table

warnings.filterwarnings("ignore")
import os
from docxtpl import DocxTemplate
from psycopg import AsyncConnection
from conv import converter
from utils import exception_response


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(BASE_DIR, "template.docx")
output_path = os.path.join(BASE_DIR, "final.docx")
business_contacts_table_path = os.path.join(BASE_DIR, "business_contacts_table.docx")
distribution_list_path = os.path.join(BASE_DIR, "distribution_list_table.docx")



async def generate_draft_engagement_letter_model(
    engagement_id: str,
    connection: AsyncConnection,
):
    audit_background_path = os.path.join(BASE_DIR, f"{engagement_id}-audit_background.docx")
    key_legislations_path = os.path.join(BASE_DIR, f"{engagement_id}-key_legislations.docx")
    key_changes_path = os.path.join(BASE_DIR, f"{engagement_id}-key_changes.docx")
    system_path = os.path.join(BASE_DIR, f"{engagement_id}-system.docx")
    reliance_path = os.path.join(BASE_DIR, f"{engagement_id}-reliance.docx")
    audit_objectives_path = os.path.join(BASE_DIR, f"{engagement_id}-audit_objectives.docx")



    with exception_response():
        data = await get_engagement_report_details(
            connection=connection,
            engagement_id=engagement_id
        )


        doc = DocxTemplate(template_path)
        business_contacts_table = Document()
        distribution_list_table = Document()




        converter(filename=audit_background_path, data=data.engagement_profile.audit_background or {})
        converter(filename=key_legislations_path, data=data.engagement_profile.key_legislations or {})
        converter(filename=key_changes_path, data=data.engagement_profile.key_changes or {})
        converter(filename=system_path, data=data.engagement_profile.relevant_systems or {})
        converter(filename=reliance_path, data=data.engagement_profile.reliance or {})
        converter(filename=audit_objectives_path, data=data.engagement_profile.audit_objectives or {})


        business_contacts_data = []
        distribution_list = []
        business_contacts_headers = ["Name", "Email", "Designation"]
        distribution_list_headers = ["Name", "Designation", "Section"]



        for __data__ in data.engagement_business_contacts:
            business_contacts_data.append([__data__.name, __data__.email, __data__.title])


        for __data__ in data.engagement_business_contacts:
            distribution_list.append([__data__.name, __data__.title, "Business Contacts"])



        create_styled_table(
            business_contacts_table,
            columns=3,
            headers=business_contacts_headers,
            data=business_contacts_data,
            column_widths=[0.1, 1.5, 2.5],
            header_bg="BBC0C0",          # dark blue header
            header_font_color="000000",  # white text
            row_bg="FFFFFF",             # light blue for data rows
            alt_row_bg="FFFFFF" ,         # white for alternating rows
            row_height=0.3,
        )


        create_styled_table(
            distribution_list_table,
            columns=3,
            headers=distribution_list_headers,
            data=distribution_list,
            column_widths=[0.1, 1.5, 2.5],
            header_bg="BBC0C0",          # dark blue header
            header_font_color="000000",  # white text
            row_bg="FFFFFF",             # light blue for data rows
            alt_row_bg="FFFFFF" ,         # white for alternating rows
            row_height=0.3,
        )

        business_contacts_table.save(business_contacts_table_path)
        distribution_list_table.save(distribution_list_path)


        audit_background_sub_doc = doc.new_subdoc(audit_background_path)
        key_legislations_sub_doc = doc.new_subdoc(key_legislations_path)
        key_changes_sub_doc = doc.new_subdoc(key_changes_path)
        system_sub_doc = doc.new_subdoc(system_path)
        reliance_sub_doc = doc.new_subdoc(reliance_path)
        audit_objectives_sub_doc = doc.new_subdoc(audit_objectives_path)
        business_contacts_table_sub_doc = doc.new_subdoc(business_contacts_table_path)
        distribution_list_sub_doc = doc.new_subdoc(distribution_list_path)






        context = {
            "organization_name": data.organization_name,
            "audit_background": audit_background_sub_doc,
            "key_legislations": key_legislations_sub_doc,
            "key_changes": key_changes_sub_doc,
            "relevant_systems": system_sub_doc,
            "reliance": reliance_sub_doc,
            "audit_objectives": audit_objectives_sub_doc,
            'engagement_code': data.engagement_code,
            "engagement_name": data.engagement_name,
            "business_contact": business_contacts_table_sub_doc,
            "business_contacts": data.engagement_business_contacts,
            "distribution_list": distribution_list_sub_doc
        }


        doc.render(context)
        doc.save(output_path)

        return output_path, data.engagement_name
