import os
import shutil
import tempfile
import uuid
from fastapi import UploadFile, BackgroundTasks
from s3 import upload_file
from schemas.attachement_schemas import AttachmentCategory
from dotenv import load_dotenv


load_dotenv()

def upload_attachment(
        file: UploadFile,
        category: AttachmentCategory,
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    key: str = f"{category.value}/{uuid.uuid4()}-{file.filename}"
    public_url: str = f"https://{os.getenv('S3_BUCKET_NAME')}.s3.{os.getenv('AWS_DEFAULT_REGION')}.amazonaws.com/{key}"
    background_tasks.add_task(upload_file, temp_path, key)

    return public_url



def extract_text(doc):
    """
    Extract plain text from a TipTap/ProseMirror JSON doc.
    Handles paragraphs, bullet lists, and ordered lists.
    Gracefully skips None values (TipTap often stores nulls).
    """
    if not doc or not isinstance(doc, dict):
        return ""

    lines = []

    def walk(node, prefix="", order_num=None):
        if not node or not isinstance(node, dict):
            return

        node_type = node.get("type")

        # Paragraph
        if node_type == "paragraph":
            content = node.get("content") or []
            text = "".join(
                c.get("text", "") for c in content if c and c.get("type") == "text"
            )
            if text.strip():
                lines.append(prefix + text)

        # List item
        elif node_type == "listItem":
            content = node.get("content") or []
            for child in content:
                walk(child, prefix=prefix, order_num=order_num)

        # Bullet list
        elif node_type == "bulletList":
            for child in node.get("content") or []:
                walk(child, prefix=prefix + "- ", order_num=None)

        # Ordered list
        elif node_type == "orderedList":
            for idx, child in enumerate(node.get("content") or [], start=1):
                walk(child, prefix=f"{prefix}{idx}. ", order_num=idx)

        # Fallback: recurse through any other "content"
        else:
            for child in node.get("content") or []:
                walk(child, prefix=prefix, order_num=order_num)

    walk(doc)
    return "\n".join(lines)
