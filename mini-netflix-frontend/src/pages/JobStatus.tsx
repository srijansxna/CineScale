import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useJobStatus } from '../hooks'
import { Button, Card, Loader, ProgressBar, JobStatusSkeleton } from '../components'
import { slideUp, staggerContainer, cardItem, scaleIn } from '../lib/motion'
import type { JobStatus as TJobStatus } from '../types'

type Status = TJobStatus['status']

const STATUS_CFG: Record<Status, {
  label: string; icon: string
  badge: string; cardBorder: string
  barColor: 'blue' | 'green' | 'red' | 'yellow' | 'brand'
}> = {
  PENDING:    { label: 'Queued',     icon: '⏳', badge: 'bg-yellow-500/15 text-yellow-400 border border-yellow-500/30', cardBorder: 'border-yellow-500/20', barColor: 'yellow' },
  PROCESSING: { label: 'Processing', icon: '⚙️', badge: 'bg-blue-500/15   text-blue-400   border border-blue-500/30',   cardBorder: 'border-blue-500/20',   barColor: 'blue'   },
  DONE:       { label: 'Complete',   icon: '✅', badge: 'bg-green-500/15  text-green-400  border border-green-500/30',  cardBorder: 'border-green-500/20',  barColor: 'green'  },
  FAILED:     { label: 'Failed',     icon: '❌', badge: 'bg-red-500/15    text-red-400    border border-red-500/30',    cardBorder: 'border-red-500/20',    barColor: 'red'    },
}

const STEPS: { label: string; min: number }[] = [
  { label: 'Queued',                min: 0   },
  { label: 'Extracting metadata',   min: 10  },
  { label: 'Transcoding',           min: 25  },
  { label: 'Generating thumbnails', min: 80  },
  { label: 'Finalizing',            min: 95  },
  { label: 'Complete',              min: 100 },
]

function StatusBadge({ status }: { status: Status }) {
  const { icon, label, badge } = STATUS_CFG[status]
  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-semibold ${badge}`}>
      <span>{icon}</span>{label}
    </span>
  )
}

function StepList({ progress, status }: { progress: number; status: Status }) {
  const currentStep = [...STEPS].reverse().find((s) => progress >= s.min)

  return (
    <motion.ol
      variants={staggerContainer}
      initial="hidden"
      animate="visible"
      className="flex flex-col gap-2.5"
    >
      {STEPS.map((step) => {
        const done   = progress >= step.min
        const active = currentStep?.label === step.label && status === 'PROCESSING'

        return (
          <motion.li key={step.label} variants={cardItem} className="flex items-center gap-3 text-sm">
            <span className={`
              w-5 h-5 rounded-full flex-shrink-0 flex items-center justify-center text-xs font-bold
              ${done   ? 'bg-green-500 text-white'
              : active ? 'bg-blue-500/30 border border-blue-400 text-blue-400'
              :          'bg-zinc-800 text-zinc-600'}
            `}>
              {done ? '✓' : ''}
            </span>
            <span className={active ? 'text-white font-medium' : done ? 'text-zinc-300' : 'text-zinc-600'}>
              {step.label}
            </span>
            {active && (
              <span className="ml-auto flex items-center gap-1.5 text-xs text-blue-400">
                <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse" />
                in progress
              </span>
            )}
          </motion.li>
        )
      })}
    </motion.ol>
  )
}

export default function JobStatus() {
  const { jobId } = useParams<{ jobId: string }>()
  const { data: job, isLoading, isError, isTerminal } = useJobStatus(jobId ?? '')

  if (isLoading) return <JobStatusSkeleton />

  if (isError || !job) {
    return (
      <motion.div
        variants={slideUp} initial="hidden" animate="visible"
        className="max-w-xl mx-auto py-16 px-4 text-center flex flex-col items-center gap-4"
      >
        <span className="text-5xl">🔍</span>
        <p className="text-white font-semibold text-lg">Job not found</p>
        <p className="text-zinc-500 text-sm">The job ID may be invalid or expired.</p>
        <Link to="/"><Button variant="secondary" size="sm">← Back to dashboard</Button></Link>
      </motion.div>
    )
  }

  const cfg = STATUS_CFG[job.status] ?? STATUS_CFG.PENDING

  return (
    <motion.div
      variants={slideUp} initial="hidden" animate="visible"
      className="max-w-xl mx-auto py-16 px-4 flex flex-col gap-6"
    >
      {/* Header */}
      <div className="flex flex-col gap-1">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-white">Processing Job</h1>
          {job.status === 'PROCESSING' && <Loader size="sm" />}
        </div>
        <p className="text-zinc-500 text-xs font-mono truncate">{job.job_id}</p>
      </div>

      {/* Status card */}
      <motion.div variants={scaleIn} initial="hidden" animate="visible">
        <Card padding="lg" className={`flex flex-col gap-5 ${cfg.cardBorder}`}>
          <div className="flex items-center justify-between">
            <StatusBadge status={job.status} />
            <span className="text-zinc-500 text-sm tabular-nums">{job.progress}%</span>
          </div>
          <ProgressBar value={job.progress} color={cfg.barColor} showValue={false} animated={job.status === 'PROCESSING'} />
          <StepList progress={job.progress} status={job.status} />
        </Card>
      </motion.div>

      {/* Error detail */}
      {job.status === 'FAILED' && job.error && (
        <motion.div variants={scaleIn} initial="hidden" animate="visible">
          <Card padding="md" className="border-red-500/20">
            <p className="text-red-400 text-sm font-semibold mb-2">Error details</p>
            <p className="text-red-300/70 text-xs font-mono leading-relaxed break-all">{job.error}</p>
          </Card>
        </motion.div>
      )}

      {/* CTA */}
      {isTerminal && (
        <motion.div variants={slideUp} initial="hidden" animate="visible" className="flex flex-col gap-3">
          {job.status === 'DONE' && (
            <Link to={`/video/${job.video_id}`}>
              <Button className="w-full justify-center py-3">Watch Video →</Button>
            </Link>
          )}
          <Link to="/" className="text-center">
            <Button variant="ghost" className="w-full justify-center">← Back to dashboard</Button>
          </Link>
        </motion.div>
      )}

      {!isTerminal && (
        <Link to="/" className="text-zinc-600 text-sm hover:text-zinc-400 transition-colors text-center">
          ← Back to dashboard
        </Link>
      )}
    </motion.div>
  )
}
