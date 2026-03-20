type Size    = 'sm' | 'md' | 'lg'
type Variant = 'spinner' | 'dots' | 'bar'

interface Props {
  size?: Size
  variant?: Variant
  label?: string
  fullPage?: boolean
}

const spinnerSizes = { sm: 'w-4 h-4 border-2', md: 'w-8 h-8 border-2', lg: 'w-12 h-12 border-[3px]' }

function Spinner({ size = 'md' }: { size?: Size }) {
  return (
    <span
      className={`block rounded-full border-zinc-600 border-t-white animate-spin ${spinnerSizes[size]}`}
      aria-hidden="true"
    />
  )
}

function Dots() {
  return (
    <span className="flex gap-1.5 items-center" aria-hidden="true">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce"
          style={{ animationDelay: `${i * 0.15}s` }}
        />
      ))}
    </span>
  )
}

function Bar() {
  return (
    <span className="w-32 h-1 bg-zinc-800 rounded-full overflow-hidden" aria-hidden="true">
      <span className="block h-full w-1/3 bg-brand rounded-full animate-[slide_1.2s_ease-in-out_infinite]" />
    </span>
  )
}

export default function Loader({ size = 'md', variant = 'spinner', label, fullPage = false }: Props) {
  const inner = (
    <div className="flex flex-col items-center gap-3" role="status" aria-label={label ?? 'Loading'}>
      {variant === 'spinner' && <Spinner size={size} />}
      {variant === 'dots'    && <Dots />}
      {variant === 'bar'     && <Bar />}
      {label && <p className="text-zinc-400 text-sm">{label}</p>}
    </div>
  )

  if (fullPage) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-surface/80 backdrop-blur-sm z-50">
        {inner}
      </div>
    )
  }

  return inner
}
