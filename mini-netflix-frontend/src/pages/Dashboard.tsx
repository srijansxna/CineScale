import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { getVideos } from '../services'
import { Button, VideoCard, DashboardSkeleton } from '../components'
import { staggerContainer, cardItem, slideUp } from '../lib/motion'

const STATS = [
  { key: 'PROCESSING', label: 'Processing', color: 'text-blue-400',  bg: 'bg-blue-500/10'  },
  { key: 'DONE',       label: 'Done',       color: 'text-green-400', bg: 'bg-green-500/10' },
  { key: 'FAILED',     label: 'Failed',     color: 'text-red-400',   bg: 'bg-red-500/10'   },
] as const

export default function Dashboard() {
  const { data: videos, isLoading, isError, refetch } = useQuery({
    queryKey: ['videos'],
    queryFn: getVideos,
    refetchInterval: 10_000,
  })

  if (isLoading) return <DashboardSkeleton />

  const total = videos?.length ?? 0
  const counts = {
    PROCESSING: videos?.filter((v) => v.processing.status === 'PROCESSING').length ?? 0,
    DONE:       videos?.filter((v) => v.processing.status === 'DONE').length ?? 0,
    FAILED:     videos?.filter((v) => v.processing.status === 'FAILED').length ?? 0,
  }

  return (
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
          <div className="w-24 h-24 rounded-3xl bg-zinc-800/80 border border-border flex items-center justify-center text-5xl">
            🎬
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
          {videos!.map((v) => (
            <motion.div key={v.video_id} variants={cardItem}>
              <VideoCard video={v} />
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  )
}
