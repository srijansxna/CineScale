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
