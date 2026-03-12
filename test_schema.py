#!/usr/bin/env python3
"""
Test the database schema by creating sample data.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from services.api.db.postgres import async_session_maker
from services.api.db.schema import (
    Video, Job, VideoVariant, Thumbnail,
    VideoStatus, JobStatus, VariantStatus
)


async def test_schema():
    """Test schema by creating sample data."""
    print("🧪 Testing Database Schema")
    print("=" * 50)
    
    async with async_session_maker() as session:
        # Create a video
        print("\n1. Creating video...")
        video = Video(
            video_id="test-video-001",
            filename="test.mp4",
            file_path="/storage/raw/test.mp4",
            file_size=10485760,  # 10MB
            content_type="video/mp4",
            duration=120.5,
            width=1920,
            height=1080,
            codec="h264",
            bitrate=5000,
            fps=30.0,
            status=VideoStatus.UPLOADED
        )
        session.add(video)
        await session.flush()
        print(f"   ✅ Created: {video}")
        
        # Create a job
        print("\n2. Creating job...")
        job = Job(
            job_id="test-job-001",
            video_id=video.video_id,
            job_type="transcode",
            status=JobStatus.PENDING,
            progress=0
        )
        session.add(job)
        await session.flush()
        print(f"   ✅ Created: {job}")
        
        # Create variants
        print("\n3. Creating video variants...")
        variants_data = [
            ("1080p", 1920, 1080),
            ("720p", 1280, 720),
            ("480p", 854, 480),
        ]
        
        for resolution, width, height in variants_data:
            variant = VideoVariant(
                video_id=video.video_id,
                resolution=resolution,
                width=width,
                height=height,
                url=f"/api/videos/{video.video_id}/stream/{resolution}",
                status=VariantStatus.PENDING
            )
            session.add(variant)
            print(f"   ✅ Created variant: {resolution}")
        
        await session.flush()
        
        # Create thumbnails
        print("\n4. Creating thumbnails...")
        thumbnail_times = [0.0, 30.0, 60.0, 90.0]
        
        for i, timestamp in enumerate(thumbnail_times):
            thumbnail = Thumbnail(
                video_id=video.video_id,
                timestamp=timestamp,
                filename=f"thumb_{i+1}.jpg",
                file_path=f"/storage/thumbnails/{video.video_id}/thumb_{i+1}.jpg",
                url=f"/api/videos/{video.video_id}/thumbnails/thumb_{i+1}.jpg",
                width=320,
                height=180,
                format="jpg",
                is_primary=(i == 0)
            )
            session.add(thumbnail)
            print(f"   ✅ Created thumbnail at {timestamp}s")
        
        await session.commit()
        print("\n✅ All data committed successfully!")
        
        # Query and display
        print("\n" + "=" * 50)
        print("📊 Querying Data")
        print("=" * 50)
        
        # Refresh to get relationships
        await session.refresh(video, ['jobs', 'variants', 'thumbnails'])
        
        print(f"\nVideo: {video.filename}")
        print(f"  ID: {video.video_id}")
        print(f"  Size: {video.file_size:,} bytes")
        print(f"  Duration: {video.duration}s")
        print(f"  Resolution: {video.width}x{video.height}")
        print(f"  Status: {video.status.value}")
        
        print(f"\nJobs: {len(video.jobs)}")
        for job in video.jobs:
            print(f"  - {job.job_id}: {job.status.value} ({job.progress}%)")
        
        print(f"\nVariants: {len(video.variants)}")
        for variant in video.variants:
            print(f"  - {variant.resolution}: {variant.width}x{variant.height} ({variant.status.value})")
        
        print(f"\nThumbnails: {len(video.thumbnails)}")
        for thumb in video.thumbnails:
            primary = " (PRIMARY)" if thumb.is_primary else ""
            print(f"  - {thumb.filename} at {thumb.timestamp}s{primary}")
        
        print("\n✅ Schema test completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_schema())
