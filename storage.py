from azure.core.exceptions import ResourceNotFoundError
from config import AzureConfig


class StorageService:

    def __init__(self):
        config = AzureConfig()
        self.container_client = config.container_client

    def upload_file(self, file):
        blob_client = self.container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file.file, overwrite=True)
        return file.filename

    def list_files(self):
        return [blob.name for blob in self.container_client.list_blobs()]

    def download_file(self, filename: str) -> str:
        blob_client = self.container_client.get_blob_client(filename)
        try:
            stream = blob_client.download_blob()
            return stream.readall().decode("utf-8", errors="ignore")
        except ResourceNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found")

    def delete_file(self, filename: str):
        blob_client = self.container_client.get_blob_client(filename)
        try:
            blob_client.delete_blob()
        except ResourceNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found")