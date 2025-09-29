from docx import Document
from copy import deepcopy

def insert_docx_at_all_placeholders(main_doc_path, insert_doc_path, placeholder, output_path):
    main_doc = Document(main_doc_path)
    insert_doc = Document(insert_doc_path)

    # Get body element of the main document
    body = main_doc._body._element

    # Collect placeholder positions
    placeholders = []

    for i, para in enumerate(main_doc.paragraphs):
        if placeholder in para.text:
            placeholders.append((i, para._element))


    if not placeholders:
        print(f"Placeholder '{placeholder}' not found.")
        return

    # Get elements from insert_doc and clone them for multiple use
    insert_elements = [deepcopy(p._element) for p in insert_doc.paragraphs]

    # Insert at each placeholder (start from last to avoid shifting issues)
    for i, (index, p_element) in enumerate(reversed(placeholders)):
        # Remove the placeholder paragraph
        p_element.getparent().remove(p_element)

        # Insert cloned content at the right index
        for insert_elem in reversed(insert_elements):
            body.insert(index, deepcopy(insert_elem))

    # Save output
    main_doc.save(output_path)


insert_docx_at_all_placeholders(
    main_doc_path="rendered.docx",
    insert_doc_path="placeholder.docx",
    placeholder="[INSERT_CONTENT_HERE]",
    output_path="final_combined.docx"
)
