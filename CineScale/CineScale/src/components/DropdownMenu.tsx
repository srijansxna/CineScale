import { useRef, useEffect, ReactNode } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

/* ── Types ──────────────────────────────────────────────────────── */
export type MenuAlign = 'left' | 'right'

export interface MenuItem {
  label: string
  icon?: ReactNode
  /** Renders the item in a danger (red) style */
  danger?: boolean
  /** Renders a divider above this item */
  divider?: boolean
  /** Disables the item */
  disabled?: boolean
  onClick: () => void
}

interface Props {
  open: boolean
  onClose: () => void
  items: MenuItem[]
  /** Which side of the trigger to align to. Default: 'right' */
  align?: MenuAlign
  /** Extra classes on the dropdown panel */
  className?: string
}

/* ── Component ──────────────────────────────────────────────────── */
export default function DropdownMenu({ open, onClose, items, align = 'right', className = '' }: Props) {
  const ref = useRef<HTMLDivElement>(null)

  // Close on outside click
  useEffect(() => {
    if (!open) return
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) onClose()
    }
    // Use capture so it fires before any stopPropagation inside the menu
    document.addEventListener('mousedown', handler, true)
    return () => document.removeEventListener('mousedown', handler, true)
  }, [open, onClose])

  // Close on Escape
  useEffect(() => {
    if (!open) return
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    document.addEventListener('keydown', handler)
    return () => document.removeEventListener('keydown', handler)
  }, [open, onClose])

  const alignClass = align === 'right' ? 'right-0' : 'left-0'

  return (
    <div ref={ref} className="relative">
      <AnimatePresence>
        {open && (
          <motion.div
            role="menu"
            initial={{ opacity: 0, scale: 0.93, y: -6 }}
            animate={{ opacity: 1, scale: 1,    y: 0  }}
            exit={{    opacity: 0, scale: 0.93, y: -6 }}
            transition={{ duration: 0.13, ease: [0.22, 1, 0.36, 1] }}
            className={`absolute top-full mt-1.5 z-50 min-w-[160px]
                        bg-zinc-900 border border-border rounded-xl
                        shadow-[0_8px_32px_rgba(0,0,0,0.55)]
                        overflow-hidden py-1
                        ${alignClass} ${className}`}
          >
            {items.map((item, i) => (
              <div key={i}>
                {item.divider && i > 0 && (
                  <div className="h-px bg-border mx-2 my-1" />
                )}
                <button
                  role="menuitem"
                  disabled={item.disabled}
                  onClick={() => { if (!item.disabled) { item.onClick(); onClose() } }}
                  className={`w-full flex items-center gap-2.5 px-3.5 py-2.5
                              text-sm text-left transition-colors duration-150
                              disabled:opacity-40 disabled:cursor-not-allowed
                              ${item.danger
                                ? 'text-red-400 hover:bg-red-500/10 hover:text-red-300'
                                : 'text-zinc-300 hover:bg-white/5 hover:text-white'}`}
                >
                  {item.icon && (
                    <span className="w-4 h-4 flex-shrink-0 flex items-center justify-center">
                      {item.icon}
                    </span>
                  )}
                  {item.label}
                </button>
              </div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
