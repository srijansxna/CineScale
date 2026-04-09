import { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import type { VideoListItem } from '../types'
import { fmtBytes, fmtDate } from '../utils'
import StatusBadge from './StatusBadge'
import DropdownMenu from './DropdownMenu'

const API = import.meta.env.VITE_API_URL

interface Props {
  video: VideoListItem
  busy?: boolean
  onDelete?: (id: string) => void
  onTogglePin?: (id: string) => void
}

export default function VideoCard({ video, busy = false, onDelete, onTogglePin }: Props) {
  // Prefer final processed thumbnail, then the user-selected one, then 50%, then 10%
  const THUMB_INDEX: Record<string, number> = { thumbnail_10: 0, thumbnail_50: 1, thumbnail_90: 2 }
  const selectedIndex = video.default_thumbnail ? (THUMB_INDEX[video.default_thumbnail] ?? 1) : 1
  const thumb = video.final_thumbnail_url
    ?? video.thumbnails?.[selectedIndex]
    ?? video.thumbnails?.[1]
    ?? video.thumbnails?.[0]
  const status = video.processing.status
  const pinned = video.isPinned ?? false

  const [menuOpen, setMenuOpen] = useState(false)

  const menuItems = [
    {
      label: pinned ? 'Unpin' : 'Pin',
      disabled: busy,
      icon: busy ? (
        <span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin inline-block" />
      ) : (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} className="w-4 h-4">
          <path strokeLinecap="round" strokeLinejoin="round"
            d="M16 12V4h1a1 1 0 000-2H7a1 1 0 000 2h1v8l-2 2v2h5v5l1 1 1-1v-5h5v-2l-2-2z" />
        </svg>
      ),
      onClick: () => !busy && onTogglePin?.(video.video_id),
    },
    {
      label: 'Delete',
      danger: true as const,
      divider: true,
      disabled: busy,
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} className="w-4 h-4">
          <path strokeLinecap="round" strokeLinejoin="round"
            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      ),
      onClick: () => !busy && onDelete?.(video.video_id),
    },
  ]

  return (
    <motion.div
      whileHover={{ y: -4 }}
      transition={{ duration: 0.18, ease: 'easeOut' }}
      className="relative group/card"
    >
      {/* Pin indicator */}
      {pinned && (
        <div className="absolute -top-1.5 -left-1.5 z-10 w-5 h-5 rounded-full bg-brand
                        flex items-center justify-center shadow-glow pointer-events-none">
          <svg viewBox="0 0 24 24" fill="currentColor" className="w-2.5 h-2.5 text-white">
            <path d="M16 12V4h1a1 1 0 000-2H7a1 1 0 000 2h1v8l-2 2v2h5v5l1 1 1-1v-5h5v-2l-2-2z" />
          </svg>
        </div>
      )}

      {/* Three-dot trigger + dropdown */}
      <div className="absolute top-2 right-2 z-20">
        <button
          onClick={(e) => { e.preventDefault(); e.stopPropagation(); if (!busy) setMenuOpen((o) => !o) }}
          aria-label="Video options"
          aria-haspopup="true"
          aria-expanded={menuOpen}
          disabled={busy}
          className="w-7 h-7 rounded-lg bg-black/50 backdrop-blur-sm border border-white/10
                     flex items-center justify-center text-zinc-400
                     hover:text-white hover:bg-black/70
                     opacity-40 group-hover/card:opacity-100 focus:opacity-100
                     disabled:opacity-30 disabled:cursor-not-allowed
                     transition-all duration-150"
        >
          {busy ? (
            <span className="w-3.5 h-3.5 border-2 border-zinc-400 border-t-transparent rounded-full animate-spin" />
          ) : (
            <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
              <circle cx="12" cy="5" r="1.5" />
              <circle cx="12" cy="12" r="1.5" />
              <circle cx="12" cy="19" r="1.5" />
            </svg>
          )}
        </button>

        <DropdownMenu
          open={menuOpen}
          onClose={() => setMenuOpen(false)}
          items={menuItems}
          align="right"
        />
      </div>

      {/* Card link */}
      <Link
        to={`/video/${video.video_id}`}
        className={`flex flex-col bg-card border rounded-2xl overflow-hidden
                   transition-all duration-200 hover:shadow-card
                   ${pinned
            ? 'border-brand/40 shadow-[0_0_0_1px_rgba(229,9,20,0.15),0_0_20px_rgba(229,9,20,0.08)]'
            : 'border-border hover:border-zinc-600'}`}
      >
        {/* Thumbnail */}
        <div className="aspect-video bg-zinc-900 relative overflow-hidden">
          {thumb ? (
            <img
              src={thumb.startsWith('http') ? thumb : `${API}${thumb}`}
              alt={video.video_title ?? video.filename}
              loading="lazy"
              className="w-full h-full object-cover group-hover/card:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-zinc-700 select-none">
              <svg className="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
                <path strokeLinecap="round" strokeLinejoin="round"
                  d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25h-9A2.25 2.25 0 002.25 7.5v9a2.25 2.25 0 002.25 2.25z" />
              </svg>
            </div>
          )}

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

          {status === 'DONE' && (
            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover/card:opacity-100
                            flex items-center justify-center transition-opacity duration-200">
              <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm border border-white/30
                              flex items-center justify-center">
                <span className="text-white text-xl pl-0.5">▶</span>
              </div>
            </div>
          )}

          {status === 'FAILED' && (
            <div className="absolute inset-0 bg-black/65 flex items-center justify-center">
              <span className="text-3xl select-none">❌</span>
            </div>
          )}
        </div>

        {/* Info */}
        <div className="p-4 flex flex-col gap-2">
          <div className="flex items-center gap-1.5 min-w-0">
            {pinned && (
              <svg viewBox="0 0 24 24" fill="currentColor" className="w-3 h-3 text-brand flex-shrink-0">
                <path d="M16 12V4h1a1 1 0 000-2H7a1 1 0 000 2h1v8l-2 2v2h5v5l1 1 1-1v-5h5v-2l-2-2z" />
              </svg>
            )}
            <p className="text-white text-sm font-semibold truncate leading-snug">
              {video.video_title ?? video.filename}
            </p>
          </div>
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
