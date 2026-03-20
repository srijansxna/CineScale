import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { Toaster } from 'react-hot-toast'
import { AnimatePresence, motion } from 'framer-motion'
import queryClient from './lib/queryClient'
import { fadeIn } from './lib/motion'
import { Navbar } from './components'
import { Dashboard, Upload, JobStatus, VideoDetail } from './pages'

function AnimatedRoutes() {
  const location = useLocation()
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        variants={fadeIn}
        initial="hidden"
        animate="visible"
        exit="exit"
      >
        <Routes location={location}>
          <Route path="/"               element={<Dashboard />} />
          <Route path="/upload"         element={<Upload />} />
          <Route path="/job/:jobId"     element={<JobStatus />} />
          <Route path="/video/:videoId" element={<VideoDetail />} />
          <Route path="*"               element={<Navigate to="/" replace />} />
        </Routes>
      </motion.div>
    </AnimatePresence>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-surface text-white font-sans">
          <Navbar />
          <main className="pt-14">
            <AnimatedRoutes />
          </main>
        </div>

        <Toaster
          position="bottom-right"
          toastOptions={{
            style: { background: '#1f1f1f', color: '#fff', border: '1px solid #2a2a2a' },
            success: { iconTheme: { primary: '#22c55e', secondary: '#fff' } },
            error:   { iconTheme: { primary: '#ef4444', secondary: '#fff' } },
          }}
        />
      </BrowserRouter>

      {import.meta.env.DEV && (
        <ReactQueryDevtools initialIsOpen={false} buttonPosition="bottom-left" />
      )}
    </QueryClientProvider>
  )
}
