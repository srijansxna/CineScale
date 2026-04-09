import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'

const links = [
  { to: '/', label: 'Home' },
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/upload', label: 'Upload' },
]

export default function Navbar() {
  const { pathname } = useLocation()
  const [open, setOpen] = useState(false)

  const isLanding = pathname === '/'

  return (
    <nav className={`fixed top-0 inset-x-0 z-50 transition-colors duration-300
      ${isLanding
        ? 'bg-transparent border-b border-transparent'
        : 'bg-surface/90 backdrop-blur-md border-b border-border'}`}
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">

        {/* Logo */}
        <Link to="/" onClick={() => setOpen(false)}
          className="flex items-center gap-2 group flex-shrink-0"
        >
          <div className="w-7 h-7 rounded-lg bg-brand flex items-center justify-center">
            <span className="text-white text-xs font-bold pl-0.5">▶</span>
          </div>
          <span className="text-white font-bold text-base tracking-tight group-hover:text-zinc-300 transition-colors">
            CineScale
          </span>
        </Link>

        {/* Desktop links */}
        <div className="hidden sm:flex items-center gap-1">
          {links.map(({ to, label }) => {
            const active = pathname === to
            return (
              <Link
                key={to}
                to={to}
                className={`relative px-4 py-1.5 rounded-lg text-sm font-medium transition-colors
                  ${active ? 'text-white' : 'text-zinc-400 hover:text-white hover:bg-white/5'}`}
              >
                {active && (
                  <motion.span
                    layoutId="nav-pill"
                    className="absolute inset-0 bg-white/10 rounded-lg"
                    transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                  />
                )}
                <span className="relative">{label}</span>
              </Link>
            )
          })}
        </div>

        {/* Desktop CTA */}
        <div className="hidden sm:block">
          <Link to="/upload">
            <motion.button
              whileHover={{ scale: 1.04 }}
              whileTap={{ scale: 0.97 }}
              className="px-4 py-1.5 bg-brand hover:bg-brand-hover text-white text-sm
                         font-semibold rounded-lg transition-colors"
            >
              Upload →
            </motion.button>
          </Link>
        </div>

        {/* Mobile hamburger */}
        <button
          className="sm:hidden flex flex-col gap-1.5 p-2 rounded-lg hover:bg-white/5 transition-colors"
          onClick={() => setOpen((o) => !o)}
          aria-label="Toggle menu"
          aria-expanded={open}
        >
          <span className={`block w-5 h-0.5 bg-zinc-400 transition-transform duration-200 origin-center ${open ? 'translate-y-2 rotate-45' : ''}`} />
          <span className={`block w-5 h-0.5 bg-zinc-400 transition-opacity duration-200 ${open ? 'opacity-0' : ''}`} />
          <span className={`block w-5 h-0.5 bg-zinc-400 transition-transform duration-200 origin-center ${open ? '-translate-y-2 -rotate-45' : ''}`} />
        </button>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2, ease: 'easeOut' }}
            className="sm:hidden overflow-hidden border-t border-border bg-surface"
          >
            <div className="px-4 py-3 flex flex-col gap-1">
              {links.map(({ to, label }) => {
                const active = pathname === to
                return (
                  <Link
                    key={to}
                    to={to}
                    onClick={() => setOpen(false)}
                    className={`px-4 py-2.5 rounded-lg text-sm font-medium transition-colors
                      ${active ? 'text-white bg-white/10' : 'text-zinc-400 hover:text-white hover:bg-white/5'}`}
                  >
                    {label}
                  </Link>
                )
              })}
              <div className="pt-2 mt-1 border-t border-border">
                <Link to="/upload" onClick={() => setOpen(false)}>
                  <button className="w-full px-4 py-2.5 bg-brand text-white text-sm font-semibold rounded-lg">
                    Upload →
                  </button>
                </Link>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}
