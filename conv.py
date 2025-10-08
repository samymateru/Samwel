from docx import Document
from docx.shared import RGBColor
from docx.shared import Pt
from reports.utils import sanitize_for_xml


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
            font_name = mark.get("attrs", {}).get("name", "")
            if font_name:
                run.font.name = font_name
                from docx.oxml.ns import qn
                run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
        elif mtype == "color":
            color_code = mark.get("attrs", {}).get("color", "")
            if color_code:
                r, g, b = hex_to_rgb(color_code)
                run.font.color.rgb = RGBColor(r, g, b)
        elif mtype == "fontsize":
            size = mark.get("attrs", {}).get("size", "")
            if size:
                run.font.size = Pt(size)


def render_node(node, document):
    ntype = node.get("type", "")

    if ntype == "paragraph":
        p = document.add_paragraph()
        for child in node.get("content", []):
            if child.get("type") == "text":
                text_value = sanitize_for_xml(child.get("text", ""))
                run = p.add_run(text_value)
                if "marks" in child:
                    apply_marks(run, child["marks"])



    if ntype == "bullet_list":
        for item in node.get("content", []):
            p = document.add_paragraph(style='List Bullet')
            for child in item.get("content", []):
                if child.get("type") == "paragraph":
                    for c in child.get("content", []):
                        if c.get("type") == "text":
                            text_value = sanitize_for_xml(c.get("text", ""))
                            run = p.add_run(text_value)
                            if "marks" in c:
                                apply_marks(run, c["marks"])


    elif ntype == "ordered_list":
        for item in node.get("content", []):
            p = document.add_paragraph(style='List Number')
            for child in item.get("content", []):
                if child.get("type") == "paragraph":
                    for c in child.get("content", []):
                        if c.get("type") == "text":
                            text_value = sanitize_for_xml(c.get("text", ""))
                            run = p.add_run(text_value)
                            if "marks" in c:
                                apply_marks(run, c["marks"])


    elif ntype == "heading":
        level = node.get("attrs", {}).get("level", 1)
        p = document.add_paragraph(style=f'Heading {min(level, 9)}')
        for child in node.get("content", []):
            if child.get("type") == "text":
                run = p.add_run(sanitize_for_xml(child.get("text", "")))
                if "marks" in child:
                    apply_marks(run, child["marks"])



    else:
        text_content = []
        for child in node.get("content", []):
            if isinstance(child, dict) and "text" in child:
                text_content.append(sanitize_for_xml(child["text"]))
        if text_content:
            document.add_paragraph(" ".join(text_content))



def render_doc(data):
    doc = Document()
    for node in data.get("content", []):
        render_node(node, doc)
    return doc



def converter(filename, data):
    sample = render_doc(data)
    sample.save(filename)


