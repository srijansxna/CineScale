export default function SkeletonCard() {
  return (
    <div className="bg-card border border-border rounded-2xl overflow-hidden animate-pulse">
      <div className="aspect-video bg-zinc-800" />
      <div className="p-4 flex flex-col gap-3">
        <div className="h-3 bg-zinc-700 rounded-full w-3/4" />
        <div className="flex items-center justify-between">
          <div className="h-5 bg-zinc-700 rounded-full w-20" />
          <div className="h-3 bg-zinc-700 rounded-full w-12" />
        </div>
        <div className="h-3 bg-zinc-800 rounded-full w-1/3" />
      </div>
    </div>
  )
}
