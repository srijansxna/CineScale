import type { ReactNode } from "react"
import { Link } from "react-router-dom"
import { motion } from "framer-motion"
import type { Variants } from "framer-motion"
import {
  staggerContainer, staggerFast, cardItem, heroItem, slideUp, scaleIn, viewport,
} from "../lib/motion"

const heroContainer: Variants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.11, delayChildren: 0.1 } },
}

function Section({ children, className = "" }: { children: ReactNode; className?: string }) {
  return (
    <section className={"py-24 sm:py-32 px-4 section-divider " + className}>
      <div className="max-w-5xl mx-auto">{children}</div>
    </section>
  )
}

function SectionHead({ label, title, sub }: { label: string; title: string; sub?: string }) {
  return (
    <motion.div variants={slideUp} initial="hidden" whileInView="visible" viewport={viewport}
      className="text-center mb-14 sm:mb-16 flex flex-col items-center gap-3"
    >
      <span className="section-label">{label}</span>
      <h2 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">{title}</h2>
      {sub && <p className="text-zinc-500 text-sm sm:text-base max-w-md leading-relaxed">{sub}</p>}
    </motion.div>
  )
}

export default function Landing() {
  return (
    <div className="flex flex-col bg-surface">
      <section className="relative min-h-screen flex flex-col items-center justify-center text-center px-4 py-28 overflow-hidden">
        <div className="pointer-events-none absolute inset-0 -z-10">
          <motion.div initial={{ opacity: 0, scale: 0.7 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 1.6 }}
            className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] rounded-full bg-brand/8 blur-[140px]" />
          <div className="absolute inset-x-0 top-0 h-32 bg-gradient-to-b from-surface to-transparent" />
          <div className="absolute inset-x-0 bottom-0 h-48 bg-gradient-to-t from-surface to-transparent" />
        </div>

        <motion.div variants={heroContainer} initial="hidden" animate="visible"
          className="flex flex-col items-center gap-6 sm:gap-8 max-w-4xl w-full"
        >
          <motion.div variants={heroItem}>
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-brand/10 border border-brand/20 text-brand text-xs font-semibold tracking-wide">
              <span className="w-1.5 h-1.5 rounded-full bg-brand animate-pulse" />
              Distributed Video Processing Pipeline
            </span>
          </motion.div>

          <motion.h1 variants={heroItem} className="text-5xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.06]">
            <span className="text-white">Process Videos</span>
            <br />
            <span className="text-gradient">Like Netflix</span>
          </motion.h1>

          <motion.p variants={heroItem} className="text-zinc-400 text-base sm:text-xl max-w-2xl leading-relaxed">
            Upload once. Get multiple resolutions, thumbnails, and streaming-ready assets.
          </motion.p>

          <motion.div variants={heroItem} className="flex flex-wrap items-center justify-center gap-3">
            <Link to="/upload">
              <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.96 }}
                className="btn-primary px-7 py-3.5 text-base">
                Upload Video →
              </motion.button>
            </Link>
            <Link to="/dashboard">
              <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.96 }}
                className="btn-ghost px-7 py-3.5 text-base">
                View Dashboard
              </motion.button>
            </Link>
          </motion.div>

          <motion.div variants={heroItem} className="flex flex-wrap justify-center gap-x-5 gap-y-2 text-zinc-600 text-xs">
            {["FFmpeg transcoding", "Celery workers", "PostgreSQL", "Docker Compose"].map((t) => (
              <span key={t} className="flex items-center gap-1.5"><span className="text-emerald-500">✓</span> {t}</span>
            ))}
          </motion.div>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 48, scale: 0.96 }} animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.85, delay: 0.7, ease: [0.22, 1, 0.36, 1] }}
          className="relative w-full max-w-3xl mt-16"
        >
          <div className="absolute -inset-[1px] rounded-3xl bg-gradient-to-b from-brand/25 via-brand/5 to-transparent blur-sm -z-10" />
          <div className="w-full aspect-video bg-zinc-950 rounded-2xl border border-white/6 overflow-hidden shadow-[0_40px_100px_rgba(0,0,0,0.7)] relative">
            <div className="absolute bottom-0 inset-x-0 h-[3px] bg-zinc-800">
              <div className="h-full w-2/3 bg-gradient-to-r from-brand to-orange-400 rounded-full" />
            </div>
            <div className="absolute bottom-[3px] inset-x-0 px-6 py-3 flex items-center justify-between bg-gradient-to-t from-black/90 to-transparent">
              <div className="flex items-center gap-3">
                <div className="w-7 h-7 rounded-full bg-white/15 border border-white/10 flex items-center justify-center">
                  <span className="text-white text-[10px] pl-px">▶</span>
                </div>
                <span className="text-white/50 text-xs font-mono">0:06 / 0:09</span>
              </div>
              <div className="flex gap-1.5">
                {["360p", "720p", "1080p"].map((r, i) => (
                  <span key={r} className={"px-2 py-0.5 rounded-md text-xs font-semibold border " + (i === 2 ? "bg-brand/20 border-brand/40 text-brand" : "bg-zinc-800/60 border-zinc-700/60 text-zinc-500")}>{r}</span>
                ))}
              </div>
            </div>
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 pb-12">
              <div className="w-14 h-14 rounded-full bg-white/10 backdrop-blur-sm border border-white/15 flex items-center justify-center">
                <span className="text-white text-xl pl-0.5">▶</span>
              </div>
              <p className="text-zinc-600 text-xs">streaming-ready output</p>
            </div>
            <div className="absolute top-4 left-4 flex items-center gap-1.5 px-2.5 py-1 bg-emerald-500/10 border border-emerald-500/25 rounded-lg">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-emerald-400 text-xs font-semibold">DONE</span>
            </div>
          </div>
        </motion.div>
      </section>

      <Section>
        <SectionHead label="How it works" title="From upload to stream in four steps" />
        <motion.div variants={staggerContainer} initial="hidden" whileInView="visible" viewport={viewport}
          className="relative flex flex-col md:flex-row items-stretch"
        >
          <div className="hidden md:block absolute top-9 left-[calc(12.5%+2rem)] right-[calc(12.5%+2rem)] h-px bg-gradient-to-r from-transparent via-border to-transparent" />
          {[
            { n: "01", accent: "text-brand", bg: "bg-brand/10 border-brand/25", title: "Upload Video", desc: "Drop any video file. MP4, MOV, AVI, WebM and MKV all supported." },
            { n: "02", accent: "text-blue-400", bg: "bg-blue-500/10 border-blue-500/25", title: "Processing Pipeline", desc: "Celery workers run FFmpeg transcoding across all target resolutions." },
            { n: "03", accent: "text-orange-400", bg: "bg-orange-500/10 border-orange-500/25", title: "Variants + Thumbnails", desc: "360p, 720p, 1080p outputs plus three preview thumbnails generated." },
            { n: "04", accent: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/25", title: "Stream Ready Output", desc: "Switch resolutions on the fly and stream directly in the browser." },
          ].map((step, i, arr) => (
            <div key={step.n} className="flex flex-col md:flex-1 items-center relative">
              {i > 0 && <div className="md:hidden w-px h-6 bg-border self-center" />}
              <motion.div variants={cardItem} className="flex flex-col items-center text-center gap-4 px-4 py-6 w-full">
                <div className={"relative w-[72px] h-[72px] rounded-2xl border " + step.bg + " flex items-center justify-center " + step.accent}>
                  <span className="text-2xl font-bold">{i + 1}</span>
                  <span className="absolute -top-2 -right-2 w-5 h-5 rounded-full bg-surface border border-border flex items-center justify-center text-[10px] font-bold text-zinc-500">{i + 1}</span>
                </div>
                <div className="flex flex-col gap-1">
                  <p className={"text-[10px] font-mono font-bold tracking-widest " + step.accent}>{step.n}</p>
                  <h3 className="text-white font-semibold text-base">{step.title}</h3>
                  <p className="text-zinc-500 text-sm leading-relaxed max-w-[180px] mx-auto">{step.desc}</p>
                </div>
              </motion.div>
              {i < arr.length - 1 && (
                <div className="hidden md:flex absolute top-9 -right-2.5 z-10 w-5 h-5 items-center justify-center">
                  <svg viewBox="0 0 16 16" fill="none" className="w-3.5 h-3.5 text-zinc-700">
                    <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
              )}
            </div>
          ))}
        </motion.div>
      </Section>

      <Section>
        <SectionHead label="Features" title="Everything handled for you" sub="From raw upload to streaming-ready output — the entire pipeline runs automatically." />
        <motion.div variants={staggerFast} initial="hidden" whileInView="visible" viewport={viewport}
          className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-5"
        >
          {[
            { accent: "text-brand", bg: "bg-brand/10 border-brand/20", glow: "hover:shadow-[0_0_32px_rgba(229,9,20,0.12)]", border: "hover:border-brand/25", title: "Multi-resolution transcoding", desc: "Transcoded to 360p, 720p, and 1080p with FFmpeg automatically.", tags: ["360p", "720p", "1080p"] },
            { accent: "text-blue-400", bg: "bg-blue-500/10 border-blue-500/20", glow: "hover:shadow-[0_0_32px_rgba(96,165,250,0.1)]", border: "hover:border-blue-500/25", title: "Thumbnail generation", desc: "Three preview frames at 10%, 50%, and 90% of the timeline.", tags: ["10%", "50%", "90%"] },
            { accent: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/20", glow: "hover:shadow-[0_0_32px_rgba(52,211,153,0.1)]", border: "hover:border-emerald-500/25", title: "Real-time job tracking", desc: "Watch your job move through each pipeline stage live.", tags: ["PENDING", "PROCESSING", "DONE"] },
            { accent: "text-purple-400", bg: "bg-purple-500/10 border-purple-500/20", glow: "hover:shadow-[0_0_32px_rgba(192,132,252,0.1)]", border: "hover:border-purple-500/25", title: "Scalable processing", desc: "Docker Compose locally, Kubernetes in production.", tags: ["Docker", "Kubernetes"] },
          ].map(({ accent, bg, glow, border, title, desc, tags }) => (
            <motion.div key={title} variants={cardItem}
              whileHover={{ y: -5, transition: { duration: 0.2 } }}
              className={"group bg-card border border-border rounded-2xl p-5 sm:p-6 flex flex-col gap-4 transition-shadow duration-300 " + glow + " " + border}
            >
              <div className={"w-11 h-11 rounded-xl border " + bg + " flex items-center justify-center " + accent}>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3.75v4.5m0-4.5h4.5m-4.5 0L9 9M3.75 20.25v-4.5m0 4.5h4.5m-4.5 0L9 15M20.25 3.75h-4.5m4.5 0v4.5m0-4.5L15 9m5.25 11.25h-4.5m4.5 0v-4.5m0 4.5L15 15" />
                </svg>
              </div>
              <div className="flex flex-col gap-1.5">
                <h3 className="text-white font-semibold text-sm sm:text-base">{title}</h3>
                <p className="text-zinc-500 text-xs sm:text-sm leading-relaxed">{desc}</p>
              </div>
              <div className="flex flex-wrap gap-1.5 mt-auto">
                {tags.map((tag) => (
                  <span key={tag} className="px-2.5 py-0.5 bg-surface border border-border rounded-lg text-zinc-500 text-xs font-medium">{tag}</span>
                ))}
              </div>
            </motion.div>
          ))}
        </motion.div>
      </Section>

      <Section>
        <motion.div variants={slideUp} initial="hidden" whileInView="visible" viewport={viewport}
          className="flex flex-col items-center gap-6 text-center"
        >
          <span className="section-label">Built with</span>
          <div className="flex flex-wrap justify-center gap-2.5">
            {["FastAPI", "Celery", "Redis", "PostgreSQL", "FFmpeg", "React", "Docker", "Tailwind CSS"].map((t) => (
              <motion.span key={t} whileHover={{ scale: 1.08, y: -2 }} transition={{ type: "spring", stiffness: 400, damping: 20 }}
                className="px-4 py-2 bg-card border border-border rounded-xl text-zinc-400 text-sm font-medium cursor-default hover:text-white transition-colors duration-200"
              >{t}</motion.span>
            ))}
          </div>
        </motion.div>
      </Section>

      <section className="py-28 px-4 section-divider relative overflow-hidden">
        <div className="pointer-events-none absolute inset-0 -z-10">
          <motion.div initial={{ opacity: 0, scale: 0.6 }} whileInView={{ opacity: 1, scale: 1 }} viewport={viewport}
            transition={{ duration: 1.4 }}
            className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] rounded-full bg-brand/8 blur-[120px]" />
        </div>
        <motion.div variants={scaleIn} initial="hidden" whileInView="visible" viewport={viewport}
          className="max-w-2xl mx-auto flex flex-col items-center text-center gap-7"
        >
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-brand/10 border border-brand/20 text-brand text-xs font-semibold">
            <span className="w-1.5 h-1.5 rounded-full bg-brand animate-pulse" /> Ready to go
          </span>
          <h2 className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight leading-[1.1]">
            Start processing your<br /><span className="text-gradient">videos now</span>
          </h2>
          <p className="text-zinc-400 text-base sm:text-lg leading-relaxed max-w-md">
            Drop a file and the pipeline handles everything — transcoding, thumbnails, and streaming-ready output.
          </p>
          <Link to="/upload">
            <motion.button whileHover={{ scale: 1.06, boxShadow: "0 0 48px rgba(229,9,20,0.5)" }} whileTap={{ scale: 0.96 }}
              transition={{ type: "spring", stiffness: 380, damping: 18 }}
              className="btn-primary px-9 py-4 text-base"
            >
              Upload Your First Video
            </motion.button>
          </Link>
          <div className="flex items-center gap-5 text-sm text-zinc-600">
            <Link to="/dashboard" className="hover:text-zinc-300 transition-colors">View dashboard →</Link>
            <span>·</span>
            <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="hover:text-zinc-300 transition-colors">API docs →</a>
          </div>
        </motion.div>
      </section>

      <footer className="border-t border-border py-10 px-4">
        <div className="max-w-5xl mx-auto flex flex-col sm:flex-row items-center sm:items-start justify-between gap-8">
          <div className="flex flex-col items-center sm:items-start gap-2">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-md bg-brand flex items-center justify-center">
                <span className="text-white text-[10px] font-bold pl-px">▶</span>
              </div>
              <span className="text-white font-bold text-sm">CineScale</span>
            </div>
            <p className="text-zinc-600 text-xs max-w-[240px] text-center sm:text-left leading-relaxed">
              Upload videos and get back multiple resolutions, thumbnails, and streaming-ready assets.
            </p>
          </div>
          <div className="flex items-center gap-6 text-sm">
            <Link to="/upload" className="text-zinc-500 hover:text-white transition-colors">Upload</Link>
            <Link to="/dashboard" className="text-zinc-500 hover:text-white transition-colors">Dashboard</Link>
            <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="text-zinc-500 hover:text-white transition-colors">API Docs</a>
          </div>
        </div>
        <div className="max-w-5xl mx-auto mt-8 pt-6 border-t border-border/50 flex flex-col sm:flex-row items-center justify-between gap-2">
          <p className="text-zinc-700 text-xs">© {new Date().getFullYear()} CineScale. All rights reserved.</p>
          <p className="text-zinc-700 text-xs">Built with FastAPI · Celery · FFmpeg · React</p>
        </div>
      </footer>
    </div>
  )
}
