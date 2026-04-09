import { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import { saveThumbnailConfig } from '../services/api'
import Button from './Button'

const API = import.meta.env.VITE_API_URL

type ThumbKey = 'thumbnail_10' | 'thumbnail_50' | 'thumbnail_90'

const THUMB_LABELS: Record<ThumbKey, string> = {
  thumbnail_10: '10%',
  thumbnail_50: '50%',
  thumbnail_90: '90%',
}

const THUMB_KEYS: ThumbKey[] = ['thumbnail_10', 'thumbnail_50', 'thumbnail_90']

const MAX_TITLE = 30

interface Props {
  videoId: string
  thumbnails: string[]           // URL paths like /api/videos/{id}/thumbnails/xxx.jpg
  initialTitle?: string | null
  initialDefaultThumb?: string | null
  onSaved?: (finalThumbnailUrl: string, title: string, defaultThumb: string) => void
}

/** Draw title text on a canvas over a thumbnail image for live preview */
function useThumbnailPreview(
  imgSrc: string,
  title: string,
  canvasRef: React.RefObject<HTMLCanvasElement>
) {
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const img = new Image()
    img.crossOrigin = 'anonymous'
    img.src = imgSrc

    img.onload = () => {
      canvas.width = img.naturalWidth
      canvas.height = img.naturalHeight
      ctx.drawImage(img, 0, 0)

      if (!title.trim()) return

      const fontSize = Math.round(img.naturalHeight / 12)
      ctx.font = `bold ${fontSize}px Oswald, Impact, sans-serif`
      ctx.textAlign = 'center'
      ctx.textBaseline = 'bottom'

      const x = img.naturalWidth / 2
      const y = img.naturalHeight - fontSize * 0.8

      // Stroke (border)
      ctx.strokeStyle = '#000000'
      ctx.lineWidth = Math.max(2, Math.round(fontSize / 14))
      ctx.lineJoin = 'round'
      ctx.strokeText(title, x, y)

      // Fill
      ctx.fillStyle = '#FFFF00'
      ctx.fillText(title, x, y)
    }
  }, [imgSrc, title, canvasRef])
}

function ThumbnailPreviewCanvas({ src, title }: { src: string; title: string }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  useThumbnailPreview(src, title, canvasRef)
  return (
    <canvas
      ref={canvasRef}
      className="w-full h-full object-cover"
      style={{ display: 'block' }}
    />
  )
}

export default function ThumbnailSelector({
  videoId,
  thumbnails,
  initialTitle,
  initialDefaultThumb,
  onSaved,
}: Props) {
  const [selected, setSelected] = useState<ThumbKey>(
    (initialDefaultThumb as ThumbKey) ?? 'thumbnail_50'
  )
  const [title, setTitle] = useState(initialTitle ?? '')
  const [saving, setSaving] = useState(false)
  const [titleError, setTitleError] = useState('')

  // Map ThumbKey → URL path
  const thumbMap: Partial<Record<ThumbKey, string>> = {}
  THUMB_KEYS.forEach((key, i) => {
    if (thumbnails[i]) thumbMap[key] = thumbnails[i]
  })

  const selectedSrc = thumbMap[selected] ? `${API}${thumbMap[selected]}` : ''

  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value
    setTitle(val)
    if (val.length > MAX_TITLE) {
      setTitleError(`Title must be ${MAX_TITLE} characters or fewer`)
    } else {
      setTitleError('')
    }
  }

  const handleSave = async () => {
    if (titleError || !title.trim()) {
      setTitleError(title.trim() ? titleError : 'Please enter a title')
      return
    }
    setSaving(true)
    try {
      const result = await saveThumbnailConfig(videoId, {
        default_thumbnail: selected,
        video_title: title.trim(),
      })
      toast.success('Thumbnail & title saved')
      onSaved?.(result.final_thumbnail_url ?? '', result.video_title, result.default_thumbnail)
    } catch {
      // axios interceptor shows the toast
    } finally {
      setSaving(false)
    }
  }

  if (thumbnails.length === 0) return null

  return (
    <div className="flex flex-col gap-5">
      <h2 className="text-white font-semibold">Thumbnail & Title</h2>

      {/* Thumbnail grid */}
      <div className="grid grid-cols-3 gap-3">
        {THUMB_KEYS.map((key) => {
          const src = thumbMap[key]
          if (!src) return null
          const isSelected = selected === key
          return (
            <motion.button
              key={key}
              whileHover={{ scale: 1.03 }}
              onClick={() => setSelected(key)}
              className={`
                relative aspect-video rounded-xl overflow-hidden bg-zinc-800 cursor-pointer
                ring-2 transition-all duration-150
                ${isSelected ? 'ring-brand shadow-lg shadow-brand/20' : 'ring-transparent hover:ring-zinc-600'}
              `}
              aria-label={`Select thumbnail at ${THUMB_LABELS[key]}`}
              aria-pressed={isSelected}
            >
              <img
                src={`${API}${src}`}
                alt={`Thumbnail at ${THUMB_LABELS[key]}`}
                className="w-full h-full object-cover"
              />
              {/* Label */}
              <span className="absolute bottom-1.5 left-1/2 -translate-x-1/2 text-xs font-semibold bg-black/60 text-white px-2 py-0.5 rounded-full">
                {THUMB_LABELS[key]}
              </span>
              {/* Selected checkmark */}
              {isSelected && (
                <span className="absolute top-1.5 right-1.5 w-5 h-5 rounded-full bg-brand flex items-center justify-center text-white text-xs font-bold shadow">
                  ✓
                </span>
              )}
            </motion.button>
          )
        })}
      </div>

      {/* Title input */}
      <div className="flex flex-col gap-1.5">
        <div className="flex items-center justify-between">
          <label className="text-zinc-400 text-sm font-medium" htmlFor="video-title-input">
            Custom title overlay
          </label>
          <span className={`text-xs tabular-nums ${title.length > MAX_TITLE ? 'text-red-400' : 'text-zinc-500'}`}>
            {title.length}/{MAX_TITLE}
          </span>
        </div>
        <input
          id="video-title-input"
          type="text"
          value={title}
          onChange={handleTitleChange}
          maxLength={MAX_TITLE + 5} // allow typing past limit to show error
          placeholder="Enter video title…"
          className={`
            w-full bg-zinc-800 border rounded-xl px-4 py-2.5 text-white text-sm
            placeholder:text-zinc-600 outline-none transition-colors
            focus:ring-2 focus:ring-brand/50
            ${titleError ? 'border-red-500' : 'border-zinc-700 focus:border-brand'}
          `}
        />
        {titleError && (
          <p className="text-red-400 text-xs">{titleError}</p>
        )}
      </div>

      {/* Live preview */}
      {selectedSrc && (
        <div className="flex flex-col gap-2">
          <p className="text-zinc-400 text-sm font-medium">Live preview</p>
          <div className="aspect-video rounded-xl overflow-hidden bg-zinc-900 ring-1 ring-white/5">
            <ThumbnailPreviewCanvas src={selectedSrc} title={title} />
          </div>
        </div>
      )}

      {/* Save button */}
      <Button
        onClick={handleSave}
        disabled={saving || !!titleError || !title.trim()}
        className="self-start"
      >
        {saving ? 'Saving…' : 'Apply & Save'}
      </Button>
    </div>
  )
}
