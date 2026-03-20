type Color = 'brand' | 'blue' | 'green' | 'red' | 'yellow'

interface Props {
  value: number       // 0–100
  label?: string
  showValue?: boolean
  color?: Color
  size?: 'sm' | 'md'
  animated?: boolean
}

const colors: Record<Color, string> = {
  brand:  'bg-brand',
  blue:   'bg-blue-500',
  green:  'bg-green-500',
  red:    'bg-red-500',
  yellow: 'bg-yellow-500',
}

const heights = { sm: 'h-1', md: 'h-2' }

export default function ProgressBar({
  value,
  label,
  showValue = true,
  color = 'brand',
  size = 'md',
  animated = false,
}: Props) {
  const clamped = Math.min(100, Math.max(0, value))

  return (
    <div className="w-full flex flex-col gap-1">
      {(label || showValue) && (
        <div className="flex justify-between items-center text-xs text-zinc-400">
          {label && <span>{label}</span>}
          {showValue && <span className="tabular-nums">{clamped}%</span>}
        </div>
      )}
      <div className={`w-full bg-zinc-800 rounded-full overflow-hidden ${heights[size]}`}>
        <div
          role="progressbar"
          aria-valuenow={clamped}
          aria-valuemin={0}
          aria-valuemax={100}
          className={`h-full rounded-full transition-all duration-500 ${colors[color]} ${animated ? 'animate-pulse' : ''}`}
          style={{ width: `${clamped}%` }}
        />
      </div>
    </div>
  )
}
