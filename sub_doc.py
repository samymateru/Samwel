from docxtpl import DocxTemplate, Subdoc

doc = DocxTemplate("finding_template.docx")


def create_final_data(context):
    subdoc1 = doc.new_subdoc("name.docx")

    doc.render(context)
    doc.save("final_output.docx")
