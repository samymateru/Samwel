from PyPDF2 import PdfReader, PdfWriter

# Load the original and replacement PDFs
original_reader = PdfReader("original.pdf")
replacement_reader = PdfReader("replace.pdf")

page_eg = 8
page_ni = 9
page_fou = 14
page_fi = 15
page_si = 16
page_sev = 17



# Create a writer and loop through the original pages
writer = PdfWriter()
for i in range(len(original_reader.pages)):
    if i == page_eg:
        writer.add_page(replacement_reader.pages[0])
        continue
    if i == page_ni:
        writer.add_page(replacement_reader.pages[1])
        continue
    if i == page_fou:
        writer.add_page(replacement_reader.pages[2])
        continue
    if i == page_fi:
        writer.add_page(replacement_reader.pages[3])
        continue
    if i == page_si:
        writer.add_page(replacement_reader.pages[4])
        continue
    if i == page_sev:
        writer.add_page(replacement_reader.pages[5])
        continue
    else:
        # Keep the original page
        writer.add_page(original_reader.pages[i])

# Save to a new PDF file
with open("output_replaced.pdf", "wb") as f:
    writer.write(f)

