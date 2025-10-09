from typing import List
from io import BytesIO
from docx import Document
from docx.shared import Pt, Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Font settings
FONT_NAME = "Arial Narrow"
FONT_SIZE = 12

# Map effectiveness to background color (cell background)
effectiveness_bg_colors = {
    "Effective": "00FF00",           # Green
    "Partially Effective": "FFFF00", # Yellow
    "Ineffective": "FF0000",         # Red
}

def set_cell_background(cell, hex_color):
    """Set the background color of a table cell in docx."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def process_summary_page(programs: List, filename_or_buffer):
    """
    Create a process summary table document.
    If `filename_or_buffer` is a BytesIO, it writes in-memory.
    Otherwise, it treats it as a path string and saves to file.
    """
    document = Document()
    headers = ["Procedure", "Effectiveness", "Total Findings"]

    # Numbering main programs
    for idx, program in enumerate(programs, start=1):
        document.add_paragraph(f"{idx}. {program['program']}", style="Heading 2")

        sub_programs = program.get("sub_programs", [])
        if not sub_programs:
            p = document.add_paragraph("No sub-programs available.")
            p.paragraph_format.left_indent = Inches(0.3)
            continue

        table = document.add_table(rows=1, cols=len(headers))
        table.style = "Table Grid"

        # Header row
        hdr_cells = table.rows[0].cells
        for i, header in enumerate(headers):
            run = hdr_cells[i].paragraphs[0].add_run(header)
            run.bold = True
            run.font.name = FONT_NAME
            run.font.size = Pt(FONT_SIZE)

        # Populate rows
        for sub in sub_programs:
            row_cells = table.add_row().cells
            row_cells[0].text = sub.get("title", "")
            row_cells[1].text = sub.get("effectiveness", "")
            row_cells[2].text = str(sub.get("issue_counts", {}).get("total", 0))

            # Apply font to all cells
            for cell in row_cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.name = FONT_NAME
                        run.font.size = Pt(FONT_SIZE)

            # Set background color for Effectiveness column
            eff_text = sub.get("effectiveness", "")
            if eff_text in effectiveness_bg_colors:
                set_cell_background(row_cells[1], effectiveness_bg_colors[eff_text])

        document.add_paragraph()  # spacing

    # Save either to file path or BytesIO
    if isinstance(filename_or_buffer, BytesIO):
        document.save(filename_or_buffer)
        filename_or_buffer.seek(0)  # reset buffer pointer
    else:
        document.save(filename_or_buffer)
