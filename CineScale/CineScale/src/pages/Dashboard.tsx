import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import toast from 'react-hot-toast'
import { getVideos, togglePin, deleteVideo } from '../services'
import { Button, VideoCard, DashboardSkeleton, ConfirmDialog } from '../components'
import { staggerContainer, cardItem, slideUp } from '../lib/motion'
import type { VideoListItem } from '../types'

const STATS = [
  { key: 'PROCESSING', label: 'Processing', color: 'text-blue-400',  bg: 'bg-blue-500/10'  },
  { key: 'DONE',       label: 'Done',       color: 'text-green-400', bg: 'bg-green-500/10' },
  { key: 'FAILED',     label: 'Failed',     color: 'text-red-400',   bg: 'bg-red-500/10'   },
] as const

export default function Dashboard() {
  const queryClient = useQueryClient()
  const [deleteTarget, setDeleteTarget] = useState<string | null>(null)
  const [busyId, setBusyId] = useState<string | null>(null)

  const { data: rawVideos, isLoading, isError, refetch } = useQuery({
    queryKey: ['videos'],
    queryFn: getVideos,
    refetchInterval: 10_000,
  })

  const pinMutation = useMutation({
    mutationFn: togglePin,
    onMutate: async (videoId) => {
      setBusyId(videoId)
      await queryClient.cancelQueries({ queryKey: ['videos'] })
      const previous = queryClient.getQueryData<VideoListItem[]>(['videos'])
      queryClient.setQueryData<VideoListItem[]>(['videos'], (old = []) =>
        old.map((v) => v.video_id === videoId ? { ...v, is_pinned: !v.is_pinned } : v)
      )
      return { previous }
    },
    onError: (_err, _id, ctx) => {
      if (ctx?.previous) queryClient.setQueryData(['videos'], ctx.previous)
      toast.error('Failed to update pin')
    },
    onSuccess: (updated) => {
      queryClient.setQueryData<VideoListItem[]>(['videos'], (old = []) =>
        old.map((v) => v.video_id === updated.video_id ? { ...v, is_pinned: updated.is_pinned } : v)
      )
      toast.success(updated.is_pinned ? 'Video pinned' : 'Video unpinned')
    },
    onSettled: () => setBusyId(null),
  })

  const deleteMutation = useMutation({
    mutationFn: deleteVideo,
    onMutate: async (videoId) => {
      setBusyId(videoId)
      await queryClient.cancelQueries({ queryKey: ['videos'] })
      const previous = queryClient.getQueryData<VideoListItem[]>(['videos'])
      queryClient.setQueryData<VideoListItem[]>(['videos'], (old = []) =>
        old.filter((v) => v.video_id !== videoId)
      )
      return { previous }
    },
    onError: (_err, _id, ctx) => {
      if (ctx?.previous) queryClient.setQueryData(['videos'], ctx.previous)
      toast.error('Failed to delete video')
    },
    onSuccess: () => toast.success('Video deleted'),
    onSettled: () => { setDeleteTarget(null); setBusyId(null) },
  })

  if (isLoading) return <DashboardSkeleton />

  // is_pinned comes from the API; optimistic update flips it in the cache directly
  const videos: VideoListItem[] = [...(rawVideos ?? [])]
    .map((v) => ({ ...v, isPinned: v.is_pinned }))
    .sort((a, b) => {
      if (a.isPinned !== b.isPinned) return a.isPinned ? -1 : 1
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    })

  const total = videos?.length ?? 0
  const counts = {
    PROCESSING: videos?.filter((v) => v.processing.status === 'PROCESSING').length ?? 0,
    DONE:       videos?.filter((v) => v.processing.status === 'DONE').length ?? 0,
    FAILED:     videos?.filter((v) => v.processing.status === 'FAILED').length ?? 0,
  }

  return (
    <>
      <div className="max-w-6xl mx-auto py-10 sm:py-16 px-4 sm:px-6">

        {/* Header */}
        <motion.div
          variants={slideUp} initial="hidden" animate="visible"
          className="flex items-center justify-between mb-8 gap-4"
        >
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Your Videos</h1>
            <p className="text-zinc-500 text-sm mt-1">
              {total > 0 ? `${total} video${total !== 1 ? 's' : ''}` : 'No videos yet'}
            </p>
          </div>
          <Link to="/upload">
            <Button size="sm">+ Upload</Button>
          </Link>
        </motion.div>

        {/* Stats bar */}
        {total > 0 && (
          <motion.div
            variants={staggerContainer} initial="hidden" animate="visible"
            className="grid grid-cols-3 gap-3 mb-8"
          >
            {STATS.map(({ key, label, color, bg }) => (
              <motion.div
                key={key} variants={cardItem}
                className={`${bg} border border-border rounded-xl px-4 py-3.5 flex flex-col gap-1`}
              >
                <span className={`text-2xl font-bold tabular-nums ${color}`}>{counts[key]}</span>
                <span className="text-zinc-500 text-xs font-medium">{label}</span>
              </motion.div>
            ))}
          </motion.div>
        )}

        {/* Error */}
        {isError && (
          <div className="flex items-center justify-between bg-red-500/10 border border-red-500/30
                          rounded-xl px-4 py-3 text-red-400 text-sm mb-6">
            <span>Failed to load videos.</span>
            <Button variant="ghost" size="sm" onClick={() => refetch()}>Retry</Button>
          </div>
        )}

        {/* Empty state */}
        {total === 0 && !isError && (
          <motion.div
            variants={slideUp} initial="hidden" animate="visible"
            className="flex flex-col items-center justify-center py-32 gap-6 text-center"
          >
            <div className="w-24 h-24 rounded-3xl bg-zinc-800/80 border border-border flex items-center justify-center">
              <svg className="w-10 h-10 text-zinc-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
                <path strokeLinecap="round" strokeLinejoin="round"
                  d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25h-9A2.25 2.25 0 002.25 7.5v9a2.25 2.25 0 002.25 2.25z" />
              </svg>
            </div>
            <div>
              <p className="text-white font-bold text-xl">No videos yet</p>
              <p className="text-zinc-500 text-sm mt-2 max-w-xs mx-auto leading-relaxed">
                Upload your first video and we'll transcode it to multiple resolutions automatically.
              </p>
            </div>
            <Link to="/upload">
              <Button>Upload your first video</Button>
            </Link>
          </motion.div>
        )}

        {/* Video grid */}
        {total > 0 && (
          <motion.div
            variants={staggerContainer} initial="hidden" animate="visible"
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
          >
            <AnimatePresence mode="popLayout">
              {videos.map((v) => (
                <motion.div
                  key={v.video_id}
                  variants={cardItem}
                  exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
                  layout
                >
                  <VideoCard
                    video={v}
                    busy={busyId === v.video_id}
                    onTogglePin={(id) => pinMutation.mutate(id)}
                    onDelete={(id) => setDeleteTarget(id)}
                  />
                </motion.div>
              ))}
            </AnimatePresence>
          </motion.div>
        )}
      </div>

      <ConfirmDialog
        open={deleteTarget !== null}
        title="Delete video?"
        message="This will permanently remove the video and all its transcoded files. This action cannot be undone."
        confirmLabel="Delete"
        danger
        loading={deleteMutation.isPending}
        onConfirm={() => deleteTarget && deleteMutation.mutate(deleteTarget)}
        onCancel={() => setDeleteTarget(null)}
      />
    </>
  )
}
