from docx import Document

from reports.models.issue_finding_model import create_table_of_content

# Create a new document
doc = Document()

data = [
    {'title': "name", "rating": "hello"},
    {'title': "name", "rating": "hello"},
    {'title': "name", "rating": "hello"},
]


data = create_table_of_content(
    issues=data,
    doc=doc
)


# Save template
doc.save('name.docx')
