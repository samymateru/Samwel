from docxtpl import DocxTemplate, Subdoc

doc = DocxTemplate("name.docx")

subdoc1 = doc.new_subdoc("placeholder.docx")
subdoc2 = doc.new_subdoc("placeholder.docx")



context = {
    'people': [
        {
        'name': subdoc1,
        }
    ]
}

doc.render(context)
doc.save("final_output.docx")
