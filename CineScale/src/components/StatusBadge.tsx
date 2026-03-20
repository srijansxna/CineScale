type Status = 'PENDING' | 'PROCESSING' | 'DONE' | 'FAILED'

interface Props {
  status: Status | string
  showIcon?: boolean
}

const CONFIG: Record<Status, { label: string; icon: string; classes: string }> = {
  PENDING:    { label: 'Pending',    icon: '⏳', classes: 'bg-zinc-700/60    text-zinc-300  border-zinc-600/40'   },
  PROCESSING: { label: 'Processing', icon: '⚙️', classes: 'bg-yellow-500/15  text-yellow-400 border-yellow-500/30' },
  DONE:       { label: 'Done',       icon: '✅', classes: 'bg-green-500/15   text-green-400  border-green-500/30'  },
  FAILED:     { label: 'Failed',     icon: '❌', classes: 'bg-red-500/15     text-red-400    border-red-500/30'    },
}

export default function StatusBadge({ status, showIcon = true }: Props) {
  const cfg = CONFIG[status as Status] ?? {
    label: status,
    icon: '●',
    classes: 'bg-zinc-700/60 text-zinc-400 border-zinc-600/40',
  }

  return (
    <span
      className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full
                  text-xs font-semibold border ${cfg.classes}`}
    >
      {showIcon && <span className="text-[10px] leading-none">{cfg.icon}</span>}
      {cfg.label}
    </span>
  )
}
