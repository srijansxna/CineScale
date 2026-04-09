import { useQuery } from '@tanstack/react-query'
import { getJobStatus } from '../services'
import type { JobStatus } from '../types'

const TERMINAL: JobStatus['status'][] = ['DONE', 'FAILED']
const POLL_INTERVAL_MS = 2000

export function useJobStatus(jobId: string) {
  const query = useQuery({
    queryKey: ['job', jobId],
    queryFn: () => getJobStatus(jobId),
    enabled: Boolean(jobId),
    retry: 2,
    // v5 signature: receives the Query object, return ms or false
    refetchInterval: ({ state }) => {
      const status = state.data?.status
      return status && TERMINAL.includes(status) ? false : POLL_INTERVAL_MS
    },
  })

  const isTerminal = TERMINAL.includes(query.data?.status ?? ('' as JobStatus['status']))

  return { ...query, isTerminal }
}
