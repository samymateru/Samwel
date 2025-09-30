from docx import Document
from docx.shared import RGBColor
from docx.shared import Pt

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))



def apply_marks(run, marks):
    for mark in marks:
        mtype = mark["type"]
        if mtype == "bold":
            run.bold = True
        elif mtype == "italic":
            run.italic = True
        elif mtype == "underline":
            run.underline = True
        elif mtype == "fontfamily":
            font_name = mark.get("attrs", {}).get("name")
            if font_name:
                run.font.name = font_name
                from docx.oxml.ns import qn
                run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
        elif mtype == "color":
            color_code = mark.get("attrs", {}).get("color")
            if color_code:
                r, g, b = hex_to_rgb(color_code)
                run.font.color.rgb = RGBColor(r, g, b)
        elif mtype == "fontsize":
            size = mark.get("attrs", {}).get("size")
            if size:
                run.font.size = Pt(size)


def render_node(node, document):
    ntype = node["type"]

    if ntype == "paragraph":
        p = document.add_paragraph()
        for child in node.get("content", []):
            if child["type"] == "text":
                run = p.add_run(child["text"])
                if "marks" in child:
                    apply_marks(run, child["marks"])

    elif ntype == "bullet_list":
        for item in node.get("content", []):
            p = document.add_paragraph(style='List Bullet')
            # recursively render the list item content inside this paragraph
            for child in item.get("content", []):
                if child["type"] == "paragraph":
                    # merge text inside this paragraph
                    for c in child.get("content", []):
                        if c["type"] == "text":
                            run = p.add_run(c["text"])
                            if "marks" in c:
                                apply_marks(run, c["marks"])

    elif ntype == "ordered_list":
        for item in node.get("content", []):
            p = document.add_paragraph(style='List Number')
            for child in item.get("content", []):
                if child["type"] == "paragraph":
                    for c in child.get("content", []):
                        if c["type"] == "text":
                            run = p.add_run(c["text"])
                            if "marks" in c:
                                apply_marks(run, c["marks"])


def render_doc(data):
    doc = Document()
    for node in data.get("content", []):
        render_node(node, doc)
    return doc


def converter(filename, data):
    sample = render_doc(data)
    sample.save(filename)



