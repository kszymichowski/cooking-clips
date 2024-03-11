from abc import ABC, abstractmethod
from pathlib import Path

class FileStorage(ABC):
    @abstractmethod
    def upload_file(self, file_path: str, file: bytes):
        pass


class LocalFileStorage(FileStorage):
    def upload_file(self, file_path: Path, file: bytes):
        with open(file_path, "wb") as buffer:
            buffer.write(file)