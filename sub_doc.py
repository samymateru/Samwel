from docxtpl import DocxTemplate, Subdoc

doc = DocxTemplate("name.docx")

# Create subdoc for insertion
subdoc = doc.new_subdoc("placeholder.docx")
subdoc.add_paragraph("This is inserted content.")


context = {
    'people': [
        {
        'name': subdoc,
        },
        {
        'place': subdoc,
        }
    ]
}

doc.render(context)
doc.save("final_output.docx")
