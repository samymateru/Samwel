import boto3
import os
from services.file_storage.file_storage_strategy import FileStorageStrategy
from services.logging.logger import global_logger
from dotenv import load_dotenv


load_dotenv()

BUCKET_NAME = "eauditrisk"
REGION = "eu-north-1"


class S3Storage(FileStorageStrategy):
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=REGION,
        )


    def upload(self, file_path: str, dest_path: str):
        try:
            if not BUCKET_NAME or not REGION:
                global_logger.error("Missing Aws Config For S3")
                return

            if not os.path.exists(file_path):
                global_logger.error(f"❌ File does not exist: {file_path}")
                return

            self.s3.upload_file(
                Filename=file_path,
                Bucket=BUCKET_NAME,
                Key=dest_path
            )



        except Exception as e:
            global_logger.error(f"Upload failed for {dest_path}: {e}")
            return

        finally:
            try:
                os.remove(file_path)
            except Exception as cleanup_error:
                global_logger.warning(f"⚠️ Failed to delete temp file: {file_path} | {cleanup_error}")


