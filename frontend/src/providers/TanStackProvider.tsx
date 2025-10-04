"use client"

import { queryClient } from '@/lib/queryClient'
import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

export default function TanStackProvider({ children }: Readonly<{ children: React.ReactNode }>) {
	return (
		<>
			<QueryClientProvider client={queryClient}>
				{children}
			</QueryClientProvider>
			<ReactQueryDevtools client={queryClient} initialIsOpen={false} />
		</>
	)
}