"""
Complete PostgreSQL schema for video processing pipeline.

Tables:
- videos: Core video information
- jobs: Processing job tracking
- video_variants: Different resolutions/formats
- thumbnails: Video thumbnail images
"""

from sqlalchemy import (
    Column, Integer, String, DateTime, Enum as SQLEnum, 
    ForeignKey, Float, BigInteger, Text, Boolean, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from services.api.db.postgres import Base


# Enums
class VideoStatus(str, enum.Enum):
    """Video processing status."""
    UPLOADED = "UPLOADED"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    DELETED = "DELETED"


class JobStatus(str, enum.Enum):
    """Job processing status."""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class VariantStatus(str, enum.Enum):
    """Video variant status."""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"


# Models
class Video(Base):
    """
    Core video table storing uploaded video information.
    """
    __tablename__ = "videos"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Unique Identifiers
    video_id = Column(String(36), unique=True, index=True, nullable=False, comment="UUID for video")
    
    # File Information
    filename = Column(String(255), nullable=False, comment="Original filename")
    file_path = Column(String(512), nullable=False, comment="Storage path")
    file_size = Column(BigInteger, nullable=False, comment="File size in bytes")
    content_type = Column(String(100), comment="MIME type")
    
    # Video Metadata
    duration = Column(Float, comment="Duration in seconds")
    width = Column(Integer, comment="Video width in pixels")
    height = Column(Integer, comment="Video height in pixels")
    codec = Column(String(50), comment="Video codec")
    bitrate = Column(Integer, comment="Bitrate in kbps")
    fps = Column(Float, comment="Frames per second")
    
    # Status
    status = Column(
        SQLEnum(VideoStatus), 
        default=VideoStatus.UPLOADED, 
        nullable=False,
        index=True,
        comment="Current video status"
    )
    
    # Timestamps
    upload_time = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False,
        comment="Upload timestamp"
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now()
    )
    
    # Soft Delete
    deleted_at = Column(DateTime(timezone=True), comment="Soft delete timestamp")
    
    # Relationships
    jobs = relationship("Job", back_populates="video", cascade="all, delete-orphan")
    variants = relationship("VideoVariant", back_populates="video", cascade="all, delete-orphan")
    thumbnails = relationship("Thumbnail", back_populates="video", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_video_status_created', 'status', 'created_at'),
        Index('idx_video_upload_time', 'upload_time'),
    )
    
    def __repr__(self):
        return f"<Video(id={self.id}, video_id={self.video_id}, filename={self.filename})>"


class Job(Base):
    """
    Processing jobs table tracking video processing tasks.
    """
    __tablename__ = "jobs"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Unique Identifier
    job_id = Column(String(36), unique=True, index=True, nullable=False, comment="UUID for job")
    
    # Foreign Key
    video_id = Column(
        String(36), 
        ForeignKey('videos.video_id', ondelete='CASCADE'), 
        nullable=False,
        index=True,
        comment="Reference to video"
    )
    
    # Job Information
    job_type = Column(String(50), default="transcode", comment="Job type: transcode, thumbnail, etc.")
    
    # Status
    status = Column(
        SQLEnum(JobStatus), 
        default=JobStatus.PENDING, 
        nullable=False,
        index=True,
        comment="Current job status"
    )
    
    # Progress
    progress = Column(
        Integer, 
        default=0, 
        nullable=False,
        comment="Progress percentage (0-100)"
    )
    
    # Results and Errors
    result = Column(Text, comment="JSON result data")
    error = Column(Text, comment="Error message if failed")
    
    # Worker Information
    worker_id = Column(String(100), comment="Worker that processed this job")
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now()
    )
    started_at = Column(DateTime(timezone=True), comment="When job started processing")
    completed_at = Column(DateTime(timezone=True), comment="When job completed")
    
    # Retry Information
    retry_count = Column(Integer, default=0, comment="Number of retry attempts")
    max_retries = Column(Integer, default=3, comment="Maximum retry attempts")
    
    # Relationship
    video = relationship("Video", back_populates="jobs")
    
    # Indexes
    __table_args__ = (
        Index('idx_job_status_created', 'status', 'created_at'),
        Index('idx_job_video_status', 'video_id', 'status'),
    )
    
    def __repr__(self):
        return f"<Job(id={self.id}, job_id={self.job_id}, status={self.status})>"


class VideoVariant(Base):
    """
    Video variants table storing different resolutions/formats.
    """
    __tablename__ = "video_variants"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key
    video_id = Column(
        String(36), 
        ForeignKey('videos.video_id', ondelete='CASCADE'), 
        nullable=False,
        index=True,
        comment="Reference to video"
    )
    
    # Variant Information
    resolution = Column(
        String(20), 
        nullable=False,
        comment="Resolution: 240p, 360p, 480p, 720p, 1080p, 1440p, 4k"
    )
    width = Column(Integer, nullable=False, comment="Width in pixels")
    height = Column(Integer, nullable=False, comment="Height in pixels")
    
    # File Information
    file_path = Column(String(512), comment="Storage path for variant")
    file_size = Column(BigInteger, comment="File size in bytes")
    
    # URL
    url = Column(String(512), comment="Streaming URL")
    
    # Encoding Information
    codec = Column(String(50), comment="Video codec")
    bitrate = Column(Integer, comment="Bitrate in kbps")
    fps = Column(Float, comment="Frames per second")
    
    # Status
    status = Column(
        SQLEnum(VariantStatus), 
        default=VariantStatus.PENDING, 
        nullable=False,
        index=True,
        comment="Variant processing status"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now()
    )
    
    # Relationship
    video = relationship("Video", back_populates="variants")
    
    # Indexes
    __table_args__ = (
        Index('idx_variant_video_resolution', 'video_id', 'resolution', unique=True),
        Index('idx_variant_status', 'status'),
    )
    
    def __repr__(self):
        return f"<VideoVariant(id={self.id}, video_id={self.video_id}, resolution={self.resolution})>"


class Thumbnail(Base):
    """
    Thumbnails table storing video thumbnail images.
    """
    __tablename__ = "thumbnails"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key
    video_id = Column(
        String(36), 
        ForeignKey('videos.video_id', ondelete='CASCADE'), 
        nullable=False,
        index=True,
        comment="Reference to video"
    )
    
    # Thumbnail Information
    timestamp = Column(
        Float, 
        nullable=False,
        comment="Timestamp in video (seconds)"
    )
    
    # File Information
    filename = Column(String(255), nullable=False, comment="Thumbnail filename")
    file_path = Column(String(512), comment="Storage path")
    file_size = Column(Integer, comment="File size in bytes")
    
    # URL
    url = Column(String(512), comment="Thumbnail URL")
    
    # Image Information
    width = Column(Integer, comment="Thumbnail width in pixels")
    height = Column(Integer, comment="Thumbnail height in pixels")
    format = Column(String(10), default="jpg", comment="Image format: jpg, png, webp")
    
    # Metadata
    is_primary = Column(Boolean, default=False, comment="Primary thumbnail for video")
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    
    # Relationship
    video = relationship("Video", back_populates="thumbnails")
    
    # Indexes
    __table_args__ = (
        Index('idx_thumbnail_video_timestamp', 'video_id', 'timestamp'),
        Index('idx_thumbnail_primary', 'video_id', 'is_primary'),
    )
    
    def __repr__(self):
        return f"<Thumbnail(id={self.id}, video_id={self.video_id}, timestamp={self.timestamp})>"
