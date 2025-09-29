def copy_doc_to_subdoc(doc, subdoc):
    """
    Copy paragraphs and runs from a python-docx Document into a docxtpl Subdoc,
    preserving styles and run formatting.
    """
    for para in doc.paragraphs:
        new_p = subdoc.add_paragraph(style=para.style.name if para.style else None)
        for run in para.runs:
            new_run = new_p.add_run(run.text)
            # Copy formatting
            new_run.bold = run.bold
            new_run.italic = run.italic
            new_run.underline = run.underline
            new_run.font.name = run.font.name
            new_run.font.size = run.font.size
            new_run.font.color.rgb = run.font.color.rgb
            # For East Asian fonts, need to set XML manually (optional)
            if run.font.name:
                from docx.oxml.ns import qn
                new_run._element.rPr.rFonts.set(qn('w:eastAsia'), run.font.name)