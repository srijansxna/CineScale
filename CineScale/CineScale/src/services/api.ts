import apiClient from '../lib/axios'
import type { UploadResponse, JobStatus, VideoDetail, VideoListItem } from '../types'

export const uploadVideo = (
  file: File,
  onProgress: (pct: number) => void
): Promise<UploadResponse> => {
  const form = new FormData()
  form.append('file', file)
  return apiClient
    .post<UploadResponse>('/api/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (e) => {
        if (e.total) onProgress(Math.round((e.loaded / e.total) * 100))
      },
    })
    .then((r) => r.data)
}

export const getJobStatus = (jobId: string): Promise<JobStatus> =>
  apiClient.get<JobStatus>(`/api/job/${jobId}`).then((r) => r.data)

export const getVideoDetail = (videoId: string): Promise<VideoDetail> =>
  apiClient.get<VideoDetail>(`/api/videos/${videoId}`).then((r) => r.data)

export const getVideos = (): Promise<VideoListItem[]> =>
  apiClient.get<VideoListItem[]>('/api/videos').then((r) => r.data)

export const togglePin = (videoId: string): Promise<VideoListItem> =>
  apiClient.patch<VideoListItem>(`/api/videos/${videoId}/pin`).then((r) => r.data)

export interface ThumbnailConfigPayload {
  default_thumbnail: 'thumbnail_10' | 'thumbnail_50' | 'thumbnail_90'
  video_title: string
}

export interface ThumbnailConfigResult {
  video_id: string
  video_title: string
  default_thumbnail: string
  final_thumbnail_url: string | null
}

export const saveThumbnailConfig = (
  videoId: string,
  payload: ThumbnailConfigPayload
): Promise<ThumbnailConfigResult> =>
  apiClient
    .post<ThumbnailConfigResult>(`/api/videos/${videoId}/thumbnail-config`, payload)
    .then((r) => r.data)

export const deleteVideo = (videoId: string): Promise<void> =>
  apiClient.delete(`/api/videos/${videoId}`).then(() => undefined)
