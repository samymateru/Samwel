from services.file_storage.file_storage_strategy import FileStorageStrategy


class FileUploader:
    def __init__(self, strategy: FileStorageStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: FileStorageStrategy):
        self.strategy = strategy

    def upload(self, file_path: str, dest_path: str):
        return self.strategy.upload(file_path, dest_path)