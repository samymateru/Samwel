import shutil
import tempfile
import uuid
import boto3
import os
from dotenv import load_dotenv
from fastapi import UploadFile, BackgroundTasks

from schemas.attachement_schemas import AttachmentCategory
from services.logging.logger import global_logger

load_dotenv()

BUCKET_NAME = "eauditrisk"
REGION = "eu-north-1"  # Change to your bucket's region

#Initialize S3 Client
s3 = boto3.client(
    "s3",
)


def upload_file(file_path, s3_key):
    try:

        if not BUCKET_NAME or not REGION:
            global_logger.error("Missing Aws Config For S3")
            return


        if not os.path.exists(file_path):
            global_logger.error(f"❌ File does not exist: {file_path}")
            return

        s3.upload_file(
            Filename=file_path,
            Bucket=BUCKET_NAME,
            Key=s3_key
        )


    except Exception as e:
        global_logger.error(f"Upload failed for {s3_key}: {e}")
        return

    finally:
        try:
            os.remove(file_path)
        except Exception as cleanup_error:
            global_logger.warning(f"⚠️ Failed to delete temp file: {file_path} | {cleanup_error}")





def delete_file(file_path: str):
    try:
        s3.delete_object(
            Bucket=BUCKET_NAME,
            Key=file_path
        )
    except Exception as e:
        print(f"Error de file: {e}")
        return None




        