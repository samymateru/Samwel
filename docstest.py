from docxtpl import DocxTemplate, RichText


def sanitize_text(text: str) -> str:
    if not text:
        return ""
    return "".join(c for c in text if c.isprintable() or c in "\n\t\r")



# Convert paragraph node to RichText
def json_to_richtext(node):
    rt = RichText()
    for item in node.get("content", []):
        text = sanitize_text(item.get("text", ""))
        marks = [mark["type"] for mark in item.get("marks", [])] if "marks" in item else []
        if "bold" in marks:
            rt.add(text, bold=True)
        else:
            rt.add(text)
        if item.get("type") == "hardBreak":
            rt.add("\n")
    return rt

# Convert JSON to renderable content
def render_content(data):
    content_list = []
    for node in data.get("content", []):
        node_type = node.get("type")
        if node_type == "paragraph":
            rt = json_to_richtext(node)
            content_list.append(rt)
        elif node_type == "bulletList":
            # Flatten bullet items as lines prefixed with "-"
            for li in node.get("content", []):
                for para in li.get("content", []):
                    rt = json_to_richtext(para)
                    content_list.append(f"- {rt}")
    return content_list



# Generate document
def create_doc(filename, data):
    doc = DocxTemplate("template.docx")
    rendered_content = render_content(data)
    doc.render({"content": rendered_content})
    doc.save(filename)