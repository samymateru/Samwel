import os
from dotenv import load_dotenv
from services.file_storage.local_file_storage import LocalStorage
from services.file_storage.s3_file_storage import S3Storage

load_dotenv()


def get_storage_strategy():
    """Select storage backend dynamically via env or config."""
    storage_type = os.getenv("STORAGE_TYPE", "s3").lower()

    if storage_type == "local":
        return LocalStorage(base_path="./uploads")


    # default
    return S3Storage()
