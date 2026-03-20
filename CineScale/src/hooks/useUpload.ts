import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { uploadVideo } from '../services'
import type { UploadResponse } from '../types'

export function useUpload() {
  const navigate = useNavigate()
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [result, setResult] = useState<UploadResponse | null>(null)

  const upload = async (file: File) => {
    setUploading(true)
    setUploadProgress(0)
    setResult(null)

    try {
      const data = await uploadVideo(file, setUploadProgress)
      setResult(data)
      toast.success(`Upload complete — job ${data.job_id.slice(0, 8)}… queued`)
      // brief pause so the user sees 100% before redirect
      setTimeout(() => navigate(`/job/${data.job_id}`), 800)
    } catch {
      // axios interceptor already showed the toast — just reset progress
      setUploadProgress(0)
    } finally {
      setUploading(false)
    }
  }

  return { upload, uploading, uploadProgress, result }
}
