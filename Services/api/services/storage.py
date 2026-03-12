import os
import aiofiles
from pathlib import Path
from fastapi import UploadFile
from services.api.config import get_settings

settings = get_settings()


class StorageService:
    """Handle file storage operations."""
    
    def __init__(self):
        self.raw_dir = Path(settings.storage_raw_dir)
        self.output_dir = Path(settings.storage_output_dir)
        self.thumbnails_dir = Path(settings.storage_thumbnails_dir)
        
        # Ensure directories exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.thumbnails_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_upload(self, file: UploadFile, filename: str) -> str:
        """Save uploaded file and return path."""
        file_path = self.raw_dir / filename
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return str(file_path)
    
    def get_output_dir(self, job_id: str) -> str:
        """Get output directory for a job."""
        job_output_dir = self.output_dir / job_id
        job_output_dir.mkdir(parents=True, exist_ok=True)
        return str(job_output_dir)
    
    def file_exists(self, path: str) -> bool:
        """Check if file exists."""
        return Path(path).exists()


def get_storage_service() -> StorageService:
    """Dependency for storage service."""
    return StorageService()
