import { QueryClient } from '@tanstack/react-query'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 5_000,          // data stays fresh for 5 s
      gcTime: 5 * 60 * 1_000,    // unused cache kept for 5 min
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 0,
    },
  },
})

export default queryClient
