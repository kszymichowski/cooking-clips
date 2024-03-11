from abc import ABC, abstractmethod

class FileStorage(ABC):
    @abstractmethod
    def upload_file(self, file_path: str, file: bytes):
        pass


class LocalFileStorage(FileStorage):
    def upload_file(self, file_path: str, file: bytes):
        with open(file_path, "wb") as buffer:
            buffer.write(file)