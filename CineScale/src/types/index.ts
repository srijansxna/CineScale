export interface UploadResponse {
  job_id: string
  video_id: string
  filename: string
  file_size: number
  status: string
  created_at: string
}

export interface JobStatus {
  job_id: string
  video_id: string
  status: 'PENDING' | 'PROCESSING' | 'DONE' | 'FAILED'
  progress: number
  result: Record<string, unknown> | null
  error: string | null
  created_at: string
  updated_at: string | null
}

export interface VideoMetadata {
  duration: number | null
  width: number | null
  height: number | null
  codec: string | null
  bitrate: number | null
  fps: number | null
}

export interface VideoVariant {
  resolution: string
  width: number
  height: number
  file_size: number | null
  url: string | null
  status: string
}

export interface ProcessingStatus {
  status: 'PENDING' | 'PROCESSING' | 'DONE' | 'FAILED'
  progress: number
  job_id: string
  started_at: string | null
  completed_at: string | null
  error: string | null
}

export interface VideoDetail {
  video_id: string
  filename: string
  file_size: number
  content_type: string | null
  metadata: VideoMetadata | null
  variants: VideoVariant[]
  thumbnails: string[]
  processing: ProcessingStatus
  created_at: string
  updated_at: string | null
}

export interface VideoListItem {
  video_id: string
  filename: string
  file_size: number
  content_type: string | null
  created_at: string
  processing: ProcessingStatus
  thumbnails: string[]
}
