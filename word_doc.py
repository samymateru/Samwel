from docx import Document
from pydantic import FutureDatetime


doc = Document()
doc.add_heading("My Document", level=1)
doc.add_paragraph("This is a paragraph.")

doc.save("output.docx")