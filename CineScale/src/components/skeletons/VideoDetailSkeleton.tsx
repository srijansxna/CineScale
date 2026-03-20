export default function VideoDetailSkeleton() {
  return (
    <div className="max-w-4xl mx-auto py-16 px-4 flex flex-col gap-8 animate-pulse">
      {/* Player */}
      <div className="aspect-video bg-zinc-800 rounded-2xl" />

      {/* Title + resolution */}
      <div className="flex flex-col sm:flex-row justify-between gap-4">
        <div className="flex flex-col gap-2">
          <div className="h-6 bg-zinc-800 rounded-lg w-64" />
          <div className="h-3 bg-zinc-800 rounded w-32" />
        </div>
        <div className="flex gap-2">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="h-8 bg-zinc-800 rounded-lg w-16" />
          ))}
        </div>
      </div>

      {/* Metadata card */}
      <div className="bg-card border border-border rounded-2xl p-5">
        <div className="h-4 bg-zinc-700 rounded w-20 mb-4" />
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-x-6 gap-y-5">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="flex flex-col gap-1.5">
              <div className="h-3 bg-zinc-800 rounded w-16" />
              <div className="h-4 bg-zinc-700 rounded w-24" />
            </div>
          ))}
        </div>
      </div>

      {/* Thumbnails */}
      <div className="flex flex-col gap-3">
        <div className="h-4 bg-zinc-700 rounded w-24" />
        <div className="grid grid-cols-3 gap-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="aspect-video bg-zinc-800 rounded-xl" />
          ))}
        </div>
      </div>
    </div>
  )
}
