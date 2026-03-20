import SkeletonCard from '../SkeletonCard'

export default function DashboardSkeleton() {
  return (
    <div className="max-w-6xl mx-auto py-16 px-4 animate-pulse">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex flex-col gap-2">
          <div className="h-7 bg-zinc-800 rounded-lg w-36" />
          <div className="h-3 bg-zinc-800 rounded w-16" />
        </div>
        <div className="h-9 bg-zinc-800 rounded-xl w-24" />
      </div>

      {/* Stats bar */}
      <div className="grid grid-cols-3 gap-3 mb-8">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="bg-card border border-border rounded-xl px-4 py-3 flex flex-col gap-1.5">
            <div className="h-6 bg-zinc-700 rounded w-8" />
            <div className="h-3 bg-zinc-800 rounded w-16" />
          </div>
        ))}
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {Array.from({ length: 8 }).map((_, i) => <SkeletonCard key={i} />)}
      </div>
    </div>
  )
}
