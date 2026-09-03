import os
import shutil
import hashlib
from fastapi import UploadFile

# Use a local directory to simulate object storage/MinIO for the prototype
STORAGE_DIR = os.getenv("SUTRA_STORAGE_DIR", "/tmp/sutra_storage")

class SecureStorage:
    def __init__(self):
        if not os.path.exists(STORAGE_DIR):
            os.makedirs(STORAGE_DIR, exist_ok=True)
            
    def save_file(self, file_id: str, contents: bytes) -> str:
        """Saves file to secure storage and returns the path."""
        file_path = os.path.join(STORAGE_DIR, file_id)
        with open(file_path, "wb") as f:
            f.write(contents)
        return file_path
        
    def get_file(self, file_id: str) -> bytes:
        """Retrieves file from secure storage."""
        file_path = os.path.join(STORAGE_DIR, file_id)
        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found in secure storage")
        with open(file_path, "rb") as f:
            return f.read()

storage = SecureStorage()
