from docxtpl import DocxTemplate, Subdoc

doc = DocxTemplate("name.docx")

# Create subdoc for insertion
subdoc1 = doc.new_subdoc("placeholder.docx")
subdoc2 = doc.new_subdoc("placeholder.docx")



context = {
    'people': [
        {
        'name': subdoc1,
        },
        {
        'name': subdoc2,
        }
    ]
}

doc.render(context)
doc.save("final_output.docx")
