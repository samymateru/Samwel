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