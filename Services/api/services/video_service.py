import uuid
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import aiofiles

from services.api.db.pg_models import Video, ProcessingJob, JobStatus
from services.api.db.postgres import get_db
from services.api.config import get_settings

settings = get_settings()


class VideoService:
    """Service for video and job management with PostgreSQL."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.storage_dir = Path(settings.storage_raw_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    async def create_video_and_job(
        self,
        file: UploadFile
    ) -> Tuple[Video, ProcessingJob]:
        """
        Create video record and processing job in database.
        
        Args:
            file: Uploaded video file
            
        Returns:
            Tuple of (Video, ProcessingJob)
        """
        # Generate IDs
        video_id = str(uuid.uuid4())
        job_id = str(uuid.uuid4())
        
        # Save file to storage
        file_path, file_size = await self._save_file(file, video_id)
        
        # Create video record
        video = Video(
            video_id=video_id,
            filename=file.filename,
            file_path=str(file_path),
            file_size=file_size,
            content_type=file.content_type
        )
        self.db.add(video)
        
        # Create processing job
        job = ProcessingJob(
            job_id=job_id,
            video_id=video_id,
            status=JobStatus.PENDING
        )
        self.db.add(job)
        
        # Commit to database
        await self.db.flush()
        await self.db.refresh(video)
        await self.db.refresh(job)
        
        return video, job
    
    async def _save_file(
        self,
        file: UploadFile,
        video_id: str
    ) -> Tuple[Path, int]:
        """
        Save uploaded file to storage.
        
        Args:
            file: Uploaded file
            video_id: Unique video identifier
            
        Returns:
            Tuple of (file_path, file_size)
        """
        # Generate filename with video_id
        file_extension = Path(file.filename).suffix
        filename = f"{video_id}{file_extension}"
        file_path = self.storage_dir / filename
        
        # Save file in chunks
        file_size = 0
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(1024 * 1024):  # 1MB chunks
                await f.write(chunk)
                file_size += len(chunk)
        
        return file_path, file_size
    
    async def get_video_by_id(self, video_id: str) -> Video:
        """Get video by video_id."""
        result = await self.db.execute(
            select(Video).where(Video.video_id == video_id)
        )
        return result.scalar_one_or_none()
    
    async def get_job_by_video_id(self, video_id: str) -> ProcessingJob:
        """Get job by video_id."""
        result = await self.db.execute(
            select(ProcessingJob).where(ProcessingJob.video_id == video_id)
        )
        return result.scalar_one_or_none()
        """Get job by job_id."""
        result = await self.db.execute(
            select(ProcessingJob).where(ProcessingJob.job_id == job_id)
        )
        return result.scalar_one_or_none()
    
    async def update_job_status(
        self,
        job_id: str,
        status: JobStatus,
        progress: int = None,
        result: dict = None,
        error: str = None
    ) -> ProcessingJob:
        """
        Update job status and progress.
        
        Args:
            job_id: Job identifier
            status: New job status
            progress: Progress percentage (0-100)
            result: Result data (for DONE status)
            error: Error message (for FAILED status)
        """
        job = await self.get_job_by_id(job_id)
        if job:
            job.status = status
            
            # Auto-set progress based on status if not provided
            if progress is not None:
                job.progress = max(0, min(100, progress))  # Clamp to 0-100
            else:
                # Default progress values
                if status == JobStatus.PENDING:
                    job.progress = 0
                elif status == JobStatus.PROCESSING:
                    job.progress = max(1, job.progress)  # At least 1% when processing
                elif status == JobStatus.DONE:
                    job.progress = 100
                # FAILED keeps current progress
            
            if result:
                job.result = result
            if error:
                job.error = error
            
            await self.db.flush()
            await self.db.refresh(job)
        return job
    
    async def delete_job(self, job_id: str) -> bool:
        """Delete a job by job_id."""
        job = await self.get_job_by_id(job_id)
        if job:
            await self.db.delete(job)
            await self.db.flush()
            return True
        return False


async def get_video_service(db: AsyncSession = Depends(get_db)) -> VideoService:
    """Dependency for video service."""
    return VideoService(db)
