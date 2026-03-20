import { useCallback, useId, useState } from 'react'
import { fmtBytes } from '../utils'
import Button from './Button'
import ProgressBar from './ProgressBar'

interface Props {
  onFile: (file: File) => void
  uploading: boolean
  progress: number
}

const ALLOWED_TYPES = [
  'video/mp4',
  'video/quicktime',
  'video/x-msvideo',
  'video/webm',
  'video/x-matroska',
]
const ALLOWED_EXT = 'MP4, MOV, AVI, WebM, MKV'
const MAX_BYTES = 500 * 1024 * 1024

export default function UploadBox({ onFile, uploading, progress }: Props) {
  const inputId = useId()
  const [dragging, setDragging] = useState(false)
  const [selected, setSelected] = useState<File | null>(null)
  const [error, setError] = useState('')

  const validate = (file: File): boolean => {
    if (!ALLOWED_TYPES.includes(file.type)) {
      setError(`Unsupported format. Allowed: ${ALLOWED_EXT}.`)
      return false
    }
    if (file.size > MAX_BYTES) {
      setError('File exceeds the 500 MB limit.')
      return false
    }
    setError('')
    return true
  }

  const pick = (file: File) => {
    if (validate(file)) setSelected(file)
  }

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) pick(file)
  }, [])

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setDragging(true)
  }

  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) pick(file)
    // reset so same file can be re-selected
    e.target.value = ''
  }

  const reset = () => {
    setSelected(null)
    setError('')
  }

  return (
    <div className="flex flex-col gap-4">

      {/* ── Drop zone ─────────────────────────────────────────── */}
      <label
        htmlFor={inputId}
        onDragOver={onDragOver}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        className={`
          relative flex flex-col items-center justify-center gap-4
          rounded-2xl border-2 border-dashed p-14 text-center
          cursor-pointer select-none transition-all duration-200
          ${uploading ? 'pointer-events-none opacity-60' : ''}
          ${dragging
            ? 'border-brand bg-brand/10 scale-[1.01]'
            : 'border-border bg-card hover:border-zinc-500 hover:bg-zinc-800/50'}
        `}
      >
        <input
          id={inputId}
          type="file"
          accept="video/*"
          className="sr-only"
          onChange={onInputChange}
          disabled={uploading}
        />

        {/* Icon */}
        <div className={`text-5xl transition-transform duration-200 ${dragging ? 'scale-110' : ''}`}>
          🎬
        </div>

        <div className="flex flex-col gap-1">
          <p className="text-white font-semibold text-base">
            {dragging ? 'Drop to select' : 'Drag & drop your video here'}
          </p>
          <p className="text-zinc-500 text-sm">or click to browse files</p>
        </div>

        <div className="flex items-center gap-2 text-zinc-600 text-xs">
          <span className="px-2 py-0.5 bg-zinc-800 rounded-md">{ALLOWED_EXT}</span>
          <span>·</span>
          <span>max 500 MB</span>
        </div>
      </label>

      {/* ── Validation error ──────────────────────────────────── */}
      {error && (
        <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/30 rounded-xl px-4 py-3">
          <span className="text-red-400 text-sm">⚠ {error}</span>
        </div>
      )}

      {/* ── Selected file info (idle) ─────────────────────────── */}
      {selected && !uploading && (
        <div className="flex items-center gap-4 bg-card border border-border rounded-xl px-4 py-3">
          <div className="w-10 h-10 rounded-lg bg-zinc-800 flex items-center justify-center text-xl flex-shrink-0">
            🎥
          </div>

          <div className="flex-1 min-w-0">
            <p className="text-sm text-white font-medium truncate">{selected.name}</p>
            <p className="text-xs text-zinc-500 mt-0.5">{fmtBytes(selected.size)}</p>
          </div>

          <div className="flex items-center gap-2 flex-shrink-0">
            <Button variant="ghost" size="sm" onClick={reset} disabled={uploading}>
              ✕
            </Button>
            <Button size="sm" onClick={() => onFile(selected)} disabled={uploading}>
              Upload
            </Button>
          </div>
        </div>
      )}

      {/* ── Upload in progress ────────────────────────────────── */}
      {uploading && selected && (
        <div className="bg-card border border-border rounded-xl px-4 py-4 flex flex-col gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-zinc-800 flex items-center justify-center text-xl flex-shrink-0">
              🎥
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-white font-medium truncate">{selected.name}</p>
              <p className="text-xs text-zinc-500">{fmtBytes(selected.size)}</p>
            </div>
            <span className="text-xs text-zinc-500 tabular-nums flex-shrink-0">{progress}%</span>
          </div>
          <ProgressBar value={progress} showValue={false} color="brand" animated={progress < 100} />
        </div>
      )}
    </div>
  )
}
