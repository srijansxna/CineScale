export const fmtBytes = (b: number) =>
  b >= 1e6 ? `${(b / 1e6).toFixed(1)} MB` : `${(b / 1e3).toFixed(0)} KB`

export const fmtDuration = (s: number) =>
  `${Math.floor(s / 60)}m ${Math.floor(s % 60)}s`

export const fmtDate = (s: string) =>
  new Date(s).toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
