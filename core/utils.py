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


def convert_to_capstone_email(email: str) -> str:
    """
    Convert any email address to the @capstone.co.tz domain.

    Example:
        user@gmail.com -> user@capstone.co.tz
        someone@hotmail.com -> someone@capstone.co.tz
    """
    local_part = email.split("@")[0]  # keep the username before @
    return f"{local_part}@capstone.co.tz"



def get_hits(data):
    if not data:
        return "Pending"

    record = data[0]  # only one item in your dataset
    sections = {
        "Finalization": "finalization_status_summary",
        "Reporting": "report_status_summary",
        "Profile": "profile_status_summary",
        "Planning": "planning_status_summary",
        "Fieldwork": "work_program_procedure_status_summary"
    }

    hits = []
    for name, key in sections.items():
        summary = record.get(key, {})
        completed = summary.get("completed", 0)
        in_progress = summary.get("in_progress", 0)

        if completed > 0 or in_progress > 0:
            hits.append(name)

    return ",".join(hits) if hits else "Pending"


def determine_priority_stage(stage: str) -> str:
    # Define your priority order
    priority = [
        "Administration",
        "Planning",
        "Fieldwork",
        "Reporting",
        "Finalization",
    ]

    if stage == "Pending":
        return "Pending"

    # Split the stage string into individual names
    stages = [s.strip() for s in stage.split(",")]

    # Find the one with the highest priority (last in order)
    for p in reversed(priority):
        if p in stages:
            return p

    return "Pending"  # fallback
