from docx import Document
from psycopg import AsyncConnection
from AuditNew.Internal.engagements.reporting.databases import get_summary_audit_process
from reports.utils import create_styled_table
from utils import exception_response


async def process_summary_rating_model(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        data = await get_summary_audit_process(
            connection=connection,
            engagement_id=engagement_id
        )

        for program in data:
            data = []
            main_program = [program.get("program"), ""]
            data.append(main_program)
            for sub in program.get("sub_programs"):
                sub_programs = [sub.get("title"), sub.get("effectiveness")]
                data.append(sub_programs)

            print(data)


data = [
    [['FERDIO', ''], ['IT', '']],
    [['Huelwie', ''], ['Justye', ''], ['Trigger test', '']],
    [['tery', ''], ['CHARTER', '']]
]



# doc = Document()
#
# create_styled_table(
#     table_of_content,
#     columns=3,
#     headers=table_of_content_headers,
#     data=table_of_content_data,
#     column_widths=[0.1, 1.5, 2.5],
#     header_bg="000094",  # dark blue header
#     header_font_color="FFFFFF",  # white text
#     row_bg="FFFFFF",  # light blue for data rows
#     alt_row_bg="FFFFFF",  # white for alternating rows
#     row_height=0.3
# )