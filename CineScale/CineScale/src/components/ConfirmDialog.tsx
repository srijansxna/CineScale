import { useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Button from './Button'

interface Props {
  open: boolean
  title: string
  message: string
  confirmLabel?: string
  onConfirm: () => void
  onCancel: () => void
  danger?: boolean
  loading?: boolean
}

export default function ConfirmDialog({
  open, title, message, confirmLabel = 'Confirm',
  onConfirm, onCancel, danger = false, loading = false,
}: Props) {
  const cancelRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    if (!open) return
    cancelRef.current?.focus()
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onCancel() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open, onCancel])

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          transition={{ duration: 0.15 }}
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          onClick={onCancel}
        >
          <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" />

          <motion.div
            initial={{ scale: 0.95, opacity: 0, y: 8 }}
            animate={{ scale: 1,    opacity: 1, y: 0 }}
            exit={{   scale: 0.95, opacity: 0, y: 8 }}
            transition={{ duration: 0.18, ease: 'easeOut' }}
            onClick={(e) => e.stopPropagation()}
            className="relative z-10 w-full max-w-sm bg-zinc-900 border border-border
                        rounded-2xl p-6 shadow-2xl"
          >
            <p className="text-white font-semibold text-base mb-2">{title}</p>
            <p className="text-zinc-400 text-sm leading-relaxed mb-6">{message}</p>

            <div className="flex gap-3 justify-end">
              <Button ref={cancelRef} variant="ghost" size="sm" onClick={onCancel} disabled={loading}>
                Cancel
              </Button>
              <Button
                size="sm"
                onClick={onConfirm}
                disabled={loading}
                className={danger ? 'bg-red-600 hover:bg-red-500 focus-visible:ring-red-500' : ''}
              >
                {loading ? 'Deleting…' : confirmLabel}
              </Button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
