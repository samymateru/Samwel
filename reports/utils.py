import warnings
warnings.filterwarnings("ignore")
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ROW_HEIGHT_RULE, WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import RGBColor, Pt, Inches



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
            run.font.color.rgb = [RGBColor.from_string(color_hex)]




def create_styled_table(
    doc,
    columns: int,
    headers: list[str],
    data: list[list[str]],
    column_widths: list[float] = None,
    header_bg: str = "00FFC0",
    header_font_color: str = "FFFFFF",
    row_bg: str = None,
    alt_row_bg: str = None,
    full_width: bool = True,
    row_height: float = None
):
    """
    Create a full-width, centered Word table with styled header and rows.
    """

    # --- Create table ---
    table = doc.add_table(rows=1, cols=columns)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER  # ✅ Center table on page


    # Disable auto-fit so we can control width
    table.autofit = False


    # --- Compute total width (defaults to full page width) ---
    if full_width:
        total_width = Inches(7)  # Typical content width for A4/Letter
        col_width = total_width / columns
        column_widths = [col_width] * columns


    elif not column_widths:
        column_widths = [Inches(1.5)] * columns  # fallback


    # --- Header Row ---
    header_row = table.rows[0]
    header_row.height = Inches(row_height)
    header_row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    hdr_cells = table.rows[0].cells

    for i, header_text in enumerate(headers):
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(header_text)
        run.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor.from_string(header_font_color)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        # Set header background color
        shading = parse_xml(
            f'<w:shd {nsdecls("w")} w:fill="{header_bg}"/>'
        )

        hdr_cells[i]._element.get_or_add_tcPr().append(shading)
        hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        # Apply column width
        hdr_cells[i].width = column_widths[i]

    # --- Data Rows ---
    for row_index, row_data in enumerate(data):

        row = table.add_row()  # row object
        if row_height:
            row.height = Inches(row_height)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST


        row_cells = row.cells

        for j, cell_value in enumerate(row_data):
            p = row_cells[j].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(str(cell_value))
            run.font.size = Pt(10)
            row_cells[j].vertical_alignment = WD_ALIGN_VERTICAL.CENTER


            # Alternate or uniform background colors
            bg_color = None
            if alt_row_bg and row_index % 2 == 1:
                bg_color = alt_row_bg
            elif row_bg:
                bg_color = row_bg

            if bg_color:
                shading = parse_xml(
                    f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>'
                )

                row_cells[j]._element.get_or_add_tcPr().append(shading)

                shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_shading(cell_value)}"/>')

                row_cells[j]._element.get_or_add_tcPr().append(shading_elm)


            row_cells[j].width = column_widths[j]

    return table


def color_shading(value: str):
    rating_map = {
        "Unacceptable": "FF0000",
        "Significant Improvement Required": "FF22FF",
        "Improvement Required": "FFFF00",
        "Acceptable": "9250D0"
    }

    return rating_map.get(value) or "FFFFFF"



#
# doc = Document()
#
#
# headers = ["Name", "Role", "Email"]
#
#
# data = [
#     ["Gerry Trasures", "Audit Lead", "kito@gmail.com"],
#     ["Collin Wilson", "Audit Assistant", "codex6992@gmail.com"],
#     ["Lydia Nyoni", "Reviewer", "lydia@gmail.com"],
# ]
#
# create_styled_table(
#     doc,
#     columns=3,
#     headers=headers,
#     data=data,
#     column_widths=[0.1, 1.5, 2.5],
#     header_bg="000092",          # dark blue header
#     header_font_color="FFFFFF",  # white text
#     row_bg="FFFFFF",             # light blue for data rows
#     alt_row_bg="FFFFFF" ,         # white for alternating rows
#     row_height=0.3
#
# )
#
# doc.save("styled_table.docx")