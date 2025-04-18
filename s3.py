from tempfile import NamedTemporaryFile
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = "egarc"
REGION = "us-east-1"  # Change to your bucket's region

# Initialize S3 Client
s3 = boto3.client(
    "s3",
)

def upload_file(file_path, s3_key):
    try:
        # Upload file to S3
        s3.upload_file(
            Filename=file_path,
            Bucket=BUCKET_NAME,
            Key=s3_key
        )
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

        