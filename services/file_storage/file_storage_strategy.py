from abc import ABC, abstractmethod


class FileStorageStrategy(ABC):
    @abstractmethod
    def upload(self, file_path: str, dest_path: str):
        """Upload a file to a specific storage backend."""
        pass
