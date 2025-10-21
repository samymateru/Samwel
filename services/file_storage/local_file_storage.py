import shutil
import os
from services.file_storage.file_storage_strategy import FileStorageStrategy


class LocalStorage(FileStorageStrategy):
    def __init__(self, base_path: str = "uploads"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def upload(self, file_path: str, dest_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        destination = os.path.join(self.base_path, dest_path)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy(file_path, destination)
        return os.path.abspath(destination)
