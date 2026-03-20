import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { getVideoDetail } from '../services'
import { Button, StatusBadge, VideoDetailSkeleton } from '../components'
import { fmtBytes, fmtDuration } from '../utils'
import { slideUp, staggerContainer, cardItem, scaleIn } from '../lib/motion'
import type { VideoMetadata } from '../types'

const API = import.meta.env.VITE_API_URL

function VideoPlayer({ src, poster }: { src?: string; poster?: string }) {
  return (
    <div className="rounded-2xl overflow-hidden bg-zinc-950 aspect-video ring-1 ring-white/5 shadow-2xl">
      {src ? (
        <video key={src} src={src} controls className="w-full h-full" poster={poster} />
      ) : (
        <div className="w-full h-full flex flex-col items-center justify-center gap-3 text-zinc-600">
          <span className="text-6xl select-none">🎬</span>
          <p className="text-sm">No playable variant available</p>
        </div>
      )}
    </div>
  )
}

function ResolutionSelector({
  variants, active, onChange,
}: {
  variants: { resolution: string }[]
  active: string
  onChange: (r: string) => void
}) {
  if (variants.length === 0) return null
  return (
    <div className="flex gap-2 flex-wrap">
      {variants.map((v) => (
        <button
          key={v.resolution}
          onClick={() => onChange(v.resolution)}
          className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
            active === v.resolution
              ? 'bg-brand text-white'
              : 'bg-zinc-800 text-zinc-300 hover:bg-zinc-700'
          }`}
        >
          {v.resolution}
        </button>
      ))}
    </div>
  )
}

function MetadataGrid({ metadata, fileSize }: { metadata: VideoMetadata | null; fileSize: number }) {
  if (!metadata) return null
  const rows = [
    { label: 'Duration',   value: metadata.duration ? fmtDuration(metadata.duration) : '—' },
    { label: 'Resolution', value: metadata.width    ? `${metadata.width}x${metadata.height}` : '—' },
    { label: 'Codec',      value: metadata.codec    ?? '—' },
    { label: 'FPS',        value: metadata.fps      ? metadata.fps.toFixed(2) : '—' },
    { label: 'Bitrate',    value: metadata.bitrate  ? `${metadata.bitrate} kbps` : '—' },
    { label: 'File size',  value: fmtBytes(fileSize) },
  ]
  return (
    <motion.div
      variants={staggerContainer}
      initial="hidden"
      animate="visible"
      className="bg-card border border-border rounded-2xl p-5 grid grid-cols-2 sm:grid-cols-3 gap-4"
    >
      {rows.map(({ label, value }) => (
        <motion.div key={label} variants={cardItem}>
          <p className="text-zinc-500 text-xs mb-0.5">{label}</p>
          <p className="text-white text-sm font-medium">{value}</p>
        </motion.div>
      ))}
    </motion.div>
  )
}

function ThumbnailsGrid({ thumbnails }: { thumbnails: string[] }) {
  if (thumbnails.length === 0) return null
  return (
    <div>
      <h2 className="text-white font-semibold mb-3">Thumbnails</h2>
      <motion.div
        variants={staggerContainer}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-3 gap-3"
      >
        {thumbnails.map((t, i) => (
          <motion.div
            key={i}
            variants={cardItem}
            whileHover={{ scale: 1.03 }}
            className="aspect-video rounded-xl overflow-hidden bg-zinc-800 cursor-pointer"
          >
            <img src={`${API}${t}`} alt={`Thumbnail ${i + 1}`} className="w-full h-full object-cover" />
          </motion.div>
        ))}
      </motion.div>
    </div>
  )
}

export default function VideoDetail() {
  const { videoId } = useParams<{ videoId: string }>()
  const [activeRes, setActiveRes] = useState<string | null>(null)

  const { data: video, isLoading, isError } = useQuery({
    queryKey: ['video', videoId],
    queryFn: () => getVideoDetail(videoId!),
    enabled: Boolean(videoId),
  })

  if (isLoading) return <VideoDetailSkeleton />

  if (isError || !video) {
    return (
      <motion.div
        variants={slideUp}
        initial="hidden"
        animate="visible"
        className="max-w-4xl mx-auto py-16 px-4 text-center flex flex-col items-center gap-4"
      >
        <span className="text-5xl">🔍</span>
        <p className="text-white font-semibold text-lg">Video not found</p>
        <Link to="/"><Button variant="secondary" size="sm">Back to dashboard</Button></Link>
      </motion.div>
    )
  }

  const readyVariants = video.variants.filter((v) => v.status === 'ready' && v.url)
  const currentVariant = readyVariants.find((v) => v.resolution === activeRes) ?? readyVariants[0]
  const videoSrc  = currentVariant?.url ? `${API}${currentVariant.url}` : undefined
  const posterSrc = video.thumbnails[1]  ? `${API}${video.thumbnails[1]}` : undefined

  return (
    <motion.div
      variants={slideUp}
      initial="hidden"
      animate="visible"
      className="max-w-4xl mx-auto py-16 px-4 flex flex-col gap-8"
    >
      <motion.div variants={scaleIn} initial="hidden" animate="visible">
        <VideoPlayer src={videoSrc} poster={posterSrc} />
      </motion.div>

      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white">{video.filename}</h1>
          <p className="text-zinc-500 text-sm mt-1">
            {fmtBytes(video.file_size)} · {new Date(video.created_at).toLocaleDateString()}
          </p>
          <div className="mt-2">
            <StatusBadge status={video.processing.status} />
          </div>
        </div>
        <ResolutionSelector
          variants={readyVariants}
          active={activeRes ?? readyVariants[0]?.resolution ?? ''}
          onChange={setActiveRes}
        />
      </div>

      <MetadataGrid metadata={video.metadata} fileSize={video.file_size} />

      <ThumbnailsGrid thumbnails={video.thumbnails} />

      <Link to="/" className="text-zinc-500 text-sm hover:text-white transition-colors">
        Back to dashboard
      </Link>
    </motion.div>
  )
}
