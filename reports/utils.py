from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import RGBColor


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
