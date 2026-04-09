export default function JobStatusSkeleton() {
  return (
    <div className="max-w-xl mx-auto py-16 px-4 flex flex-col gap-6 animate-pulse">
      {/* Title */}
      <div className="flex flex-col gap-2">
        <div className="h-7 bg-zinc-800 rounded-lg w-48" />
        <div className="h-3 bg-zinc-800 rounded w-64" />
      </div>

      {/* Status card */}
      <div className="bg-card border border-border rounded-2xl p-6 flex flex-col gap-5">
        {/* Badge + percentage */}
        <div className="flex items-center justify-between">
          <div className="h-6 bg-zinc-700 rounded-full w-28" />
          <div className="h-4 bg-zinc-800 rounded w-10" />
        </div>

        {/* Progress bar */}
        <div className="h-2 bg-zinc-800 rounded-full" />

        {/* Steps */}
        <div className="flex flex-col gap-3 pt-1">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="flex items-center gap-3">
              <div className="w-5 h-5 rounded-full bg-zinc-800 flex-shrink-0" />
              <div className="h-3 bg-zinc-800 rounded" style={{ width: `${55 + (i % 3) * 15}%` }} />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
