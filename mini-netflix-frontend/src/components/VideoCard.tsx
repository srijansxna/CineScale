import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import type { VideoListItem } from '../types'
import { fmtBytes, fmtDate } from '../utils'
import StatusBadge from './StatusBadge'

const API = import.meta.env.VITE_API_URL

export default function VideoCard({ video }: { video: VideoListItem }) {
  const thumb  = video.thumbnails?.[1] ?? video.thumbnails?.[0]
  const status = video.processing.status

  return (
    <motion.div
      whileHover={{ y: -4 }}
      whileTap={{ scale: 0.98 }}
      transition={{ duration: 0.18, ease: 'easeOut' }}
    >
      <Link
        to={`/video/${video.video_id}`}
        className="group flex flex-col bg-card border border-border rounded-2xl overflow-hidden
                   hover:border-zinc-600 hover:shadow-card transition-all duration-200"
      >
        {/* Thumbnail */}
        <div className="aspect-video bg-zinc-900 relative overflow-hidden">
          {thumb ? (
            <img
              src={`${API}${thumb}`}
              alt={video.filename}
              loading="lazy"
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-zinc-700 select-none">
              <svg className="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
                <path strokeLinecap="round" strokeLinejoin="round"
                  d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25h-9A2.25 2.25 0 002.25 7.5v9a2.25 2.25 0 002.25 2.25z" />
              </svg>
            </div>
          )}

          {/* Processing overlay */}
          {status === 'PROCESSING' && (
            <div className="absolute inset-0 bg-black/65 flex flex-col items-center justify-center gap-2">
              <div className="w-7 h-7 border-2 border-white border-t-transparent rounded-full animate-spin" />
              <span className="text-white text-xs font-semibold tabular-nums">{video.processing.progress}%</span>
              <div className="absolute bottom-0 inset-x-0 h-1 bg-zinc-800">
                <div className="h-full bg-blue-500 transition-all duration-500"
                  style={{ width: `${video.processing.progress}%` }} />
              </div>
            </div>
          )}

          {/* Hover play — DONE only */}
          {status === 'DONE' && (
            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100
                            flex items-center justify-center transition-opacity duration-200">
              <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm border border-white/30
                              flex items-center justify-center">
                <span className="text-white text-xl pl-0.5">▶</span>
              </div>
            </div>
          )}

          {/* Failed overlay */}
          {status === 'FAILED' && (
            <div className="absolute inset-0 bg-black/65 flex items-center justify-center">
              <span className="text-3xl select-none">❌</span>
            </div>
          )}
        </div>

        {/* Info */}
        <div className="p-4 flex flex-col gap-2">
          <p className="text-white text-sm font-semibold truncate leading-snug">{video.filename}</p>
          <div className="flex items-center justify-between gap-2">
            <StatusBadge status={status} showIcon={false} />
            <span className="text-zinc-500 text-xs tabular-nums flex-shrink-0">{fmtBytes(video.file_size)}</span>
          </div>
          <p className="text-zinc-600 text-xs">{fmtDate(video.created_at)}</p>
        </div>
      </Link>
    </motion.div>
  )
}
