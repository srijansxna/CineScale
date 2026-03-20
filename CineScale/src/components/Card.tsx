import type { HTMLAttributes, ReactNode } from 'react'

type Padding = 'none' | 'sm' | 'md' | 'lg'

interface Props extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode
  padding?: Padding
  hoverable?: boolean
}

const paddings: Record<Padding, string> = {
  none: '',
  sm:   'p-3',
  md:   'p-5',
  lg:   'p-7',
}

export default function Card({
  children,
  padding = 'md',
  hoverable = false,
  className = '',
  ...props
}: Props) {
  return (
    <div
      className={`
        bg-card border border-border rounded-2xl
        ${paddings[padding]}
        ${hoverable ? 'hover:border-zinc-600 hover:scale-[1.02] transition-all duration-200 cursor-pointer' : ''}
        ${className}
      `}
      {...props}
    >
      {children}
    </div>
  )
}
