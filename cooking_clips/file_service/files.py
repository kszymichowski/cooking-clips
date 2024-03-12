from abc import ABC, abstractmethod
from pathlib import Path
import boto3

class FileStorage(ABC):
    @abstractmethod
    def upload_file(self, file_path: str, file: bytes):
        pass


class LocalFileStorage(FileStorage):
    def upload_file(self, file_path: Path, file: bytes):
        with open(file_path, "wb") as buffer:
            buffer.write(file)

class S3FileStorage(FileStorage):
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    def upload_file(self, file_path: str, file: bytes):
        self.s3_client.upload_fileobj(file, self.bucket_name, file_path)