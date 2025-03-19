import boto3
from dotenv import load_dotenv
import os


# AWS Credentials (Recommended: Use environment variables or IAM roles)
AWS_ACCESS_KEY = os.getenv("ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("Tn1wR1QjucjAcVMk3MjJEcs/I1VgARmJ5C23JNGF")
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
        public_url = f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{s3_key}"
        print(f"File uploaded successfully! Public URL: {public_url}")
        return public_url

    except Exception as e:
        print(f"Error uploading file: {e}")
        return None
