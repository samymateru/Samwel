import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from docxtpl import DocxTemplate, Subdoc




doc = DocxTemplate("name.docx")

# Create a context dictionary with keys matching your placeholders
context = {
    'name': "Samwel",
    'people': [
        {'name': 'Samuel', 'place': 'Python Land'},
        {'name': 'Anna', 'place': 'Data City'},
        {'name': 'Mike', 'place': 'Code Town'},
        {'name': 'Samuel', 'place': 'Python Land'},
        {'name': 'Anna', 'place': 'Data City'},
        {'name': 'Mike', 'place': 'Code Town'},
        {'name': 'Samuel', 'place': 'Python Land'},
        {'name': 'Anna', 'place': 'Data City'},
        {'name': 'Mike', 'place': 'Code Town'},
        {'name': 'Samuel', 'place': 'Python Land'},
        {'name': 'Anna', 'place': 'Data City'},
        {'name': 'Mike', 'place': 'Code Town'},
        {'name': 'Anna', 'place': 'Data City'},
        {'name': 'Mike', 'place': 'Code Town'},
        {'name': 'Samuel', 'place': 'Python Land'},
        {'name': 'Anna', 'place': 'Data City'},
        {'name': 'Mike', 'place': 'Code Town'},
        {'name': 'Anna', 'place': 'Data City'},
        {'name': 'Mike', 'place': 'Code Town'},
        {'name': 'Samuel', 'place': 'Python Land'},
        {'name': 'Anna', 'place': 'Data City'},
        {'name': 'Mike', 'place': 'Code Town'},
    ]
}

# Render the context into the template
doc.render(context)

# Save the result
doc.save("output.docx")
