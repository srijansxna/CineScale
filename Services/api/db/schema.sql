-- PostgreSQL Schema for Video Processing Pipeline
-- Generated from SQLAlchemy models

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enums
CREATE TYPE video_status AS ENUM (
    'UPLOADED',
    'QUEUED',
    'PROCESSING',
    'COMPLETED',
    'FAILED',
    'DELETED'
);

CREATE TYPE job_status AS ENUM (
    'PENDING',
    'PROCESSING',
    'DONE',
    'FAILED',
    'CANCELLED'
);

CREATE TYPE variant_status AS ENUM (
    'PENDING',
    'PROCESSING',
    'READY',
    'FAILED'
);

-- Videos Table
CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(36) UNIQUE NOT NULL,
    
    -- File Information
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(512) NOT NULL,
    file_size BIGINT NOT NULL,
    content_type VARCHAR(100),
    
    -- Video Metadata
    duration FLOAT,
    width INTEGER,
    height INTEGER,
    codec VARCHAR(50),
    bitrate INTEGER,
    fps FLOAT,
    
    -- Status
    status video_status NOT NULL DEFAULT 'UPLOADED',
    
    -- Timestamps
    upload_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    deleted_at TIMESTAMP WITH TIME ZONE,
    
    -- Indexes
    CONSTRAINT videos_video_id_key UNIQUE (video_id)
);

-- Indexes for videos
CREATE INDEX idx_videos_video_id ON videos(video_id);
CREATE INDEX idx_videos_status ON videos(status);
CREATE INDEX idx_videos_status_created ON videos(status, created_at);
CREATE INDEX idx_videos_upload_time ON videos(upload_time);

-- Jobs Table
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(36) UNIQUE NOT NULL,
    video_id VARCHAR(36) NOT NULL,
    
    -- Job Information
    job_type VARCHAR(50) DEFAULT 'transcode',
    
    -- Status
    status job_status NOT NULL DEFAULT 'PENDING',
    progress INTEGER NOT NULL DEFAULT 0,
    
    -- Results and Errors
    result TEXT,
    error TEXT,
    
    -- Worker Information
    worker_id VARCHAR(100),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    -- Retry Information
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    
    -- Foreign Key
    CONSTRAINT fk_jobs_video_id FOREIGN KEY (video_id)
        REFERENCES videos(video_id) ON DELETE CASCADE,
    
    -- Constraints
    CONSTRAINT jobs_job_id_key UNIQUE (job_id),
    CONSTRAINT jobs_progress_check CHECK (progress >= 0 AND progress <= 100)
);

-- Indexes for jobs
CREATE INDEX idx_jobs_job_id ON jobs(job_id);
CREATE INDEX idx_jobs_video_id ON jobs(video_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_status_created ON jobs(status, created_at);
CREATE INDEX idx_jobs_video_status ON jobs(video_id, status);

-- Video Variants Table
CREATE TABLE video_variants (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(36) NOT NULL,
    
    -- Variant Information
    resolution VARCHAR(20) NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    
    -- File Information
    file_path VARCHAR(512),
    file_size BIGINT,
    
    -- URL
    url VARCHAR(512),
    
    -- Encoding Information
    codec VARCHAR(50),
    bitrate INTEGER,
    fps FLOAT,
    
    -- Status
    status variant_status NOT NULL DEFAULT 'PENDING',
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    
    -- Foreign Key
    CONSTRAINT fk_video_variants_video_id FOREIGN KEY (video_id)
        REFERENCES videos(video_id) ON DELETE CASCADE,
    
    -- Unique Constraint
    CONSTRAINT video_variants_video_resolution_unique UNIQUE (video_id, resolution)
);

-- Indexes for video_variants
CREATE INDEX idx_video_variants_video_id ON video_variants(video_id);
CREATE INDEX idx_video_variants_status ON video_variants(status);
CREATE UNIQUE INDEX idx_video_variants_video_resolution ON video_variants(video_id, resolution);

-- Thumbnails Table
CREATE TABLE thumbnails (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(36) NOT NULL,
    
    -- Thumbnail Information
    timestamp FLOAT NOT NULL,
    
    -- File Information
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(512),
    file_size INTEGER,
    
    -- URL
    url VARCHAR(512),
    
    -- Image Information
    width INTEGER,
    height INTEGER,
    format VARCHAR(10) DEFAULT 'jpg',
    
    -- Metadata
    is_primary BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- Foreign Key
    CONSTRAINT fk_thumbnails_video_id FOREIGN KEY (video_id)
        REFERENCES videos(video_id) ON DELETE CASCADE
);

-- Indexes for thumbnails
CREATE INDEX idx_thumbnails_video_id ON thumbnails(video_id);
CREATE INDEX idx_thumbnails_video_timestamp ON thumbnails(video_id, timestamp);
CREATE INDEX idx_thumbnails_primary ON thumbnails(video_id, is_primary);

-- Comments
COMMENT ON TABLE videos IS 'Core video information and metadata';
COMMENT ON TABLE jobs IS 'Processing job tracking';
COMMENT ON TABLE video_variants IS 'Different video resolutions and formats';
COMMENT ON TABLE thumbnails IS 'Video thumbnail images';

COMMENT ON COLUMN videos.video_id IS 'UUID for video';
COMMENT ON COLUMN videos.file_size IS 'File size in bytes';
COMMENT ON COLUMN videos.duration IS 'Duration in seconds';
COMMENT ON COLUMN videos.upload_time IS 'Upload timestamp';

COMMENT ON COLUMN jobs.job_id IS 'UUID for job';
COMMENT ON COLUMN jobs.progress IS 'Progress percentage (0-100)';
COMMENT ON COLUMN jobs.result IS 'JSON result data';

COMMENT ON COLUMN video_variants.resolution IS 'Resolution: 240p, 360p, 480p, 720p, 1080p, 1440p, 4k';
COMMENT ON COLUMN thumbnails.timestamp IS 'Timestamp in video (seconds)';
COMMENT ON COLUMN thumbnails.is_primary IS 'Primary thumbnail for video';
