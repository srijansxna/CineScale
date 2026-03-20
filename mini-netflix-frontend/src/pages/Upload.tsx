import { motion } from 'framer-motion'
import { UploadBox } from '../components'
import { useUpload } from '../hooks'
import { slideUp, staggerContainer, cardItem } from '../lib/motion'

const features = [
  { icon: '⚡', label: 'Multi-resolution', text: 'Transcoded to 360p, 720p and 1080p' },
  { icon: '🖼', label: 'Auto thumbnails',  text: 'Generated at 10%, 50% and 90%' },
  { icon: '📊', label: 'Metadata',         text: 'Duration, codec, bitrate extracted' },
]

export default function Upload() {
  const { upload, uploading, uploadProgress } = useUpload()

  return (
    <div className="max-w-xl mx-auto py-10 sm:py-16 px-4 sm:px-6">

      {/* Header */}
      <motion.div variants={slideUp} initial="hidden" animate="visible" className="mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight mb-2">Upload Video</h1>
        <p className="text-zinc-400 text-sm leading-relaxed">
          Drop a video below to start processing. You'll be redirected to a live job status page.
        </p>
      </motion.div>

      {/* Upload box */}
      <motion.div variants={slideUp} initial="hidden" animate="visible">
        <UploadBox onFile={upload} uploading={uploading} progress={uploadProgress} />
      </motion.div>

      {/* Feature hints */}
      {!uploading && (
        <motion.ul
          variants={staggerContainer} initial="hidden" animate="visible"
          className="mt-8 flex flex-col gap-3"
        >
          {features.map(({ icon, label, text }) => (
            <motion.li
              key={label} variants={cardItem}
              className="flex items-start gap-3 bg-card border border-border rounded-xl px-4 py-3"
            >
              <span className="text-xl mt-0.5 flex-shrink-0">{icon}</span>
              <div>
                <p className="text-white text-sm font-medium">{label}</p>
                <p className="text-zinc-500 text-xs mt-0.5">{text}</p>
              </div>
            </motion.li>
          ))}
        </motion.ul>
      )}
    </div>
  )
}
