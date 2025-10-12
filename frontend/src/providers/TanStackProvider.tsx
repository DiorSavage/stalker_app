"use client"

import { queryClient } from '@/lib/queryClient'
import { YMaps } from '@pbe/react-yandex-maps'
import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import Script from 'next/script'

export default function TanStackProvider({ children }: Readonly<{ children: React.ReactNode }>) {

	const apiKey = process.env.NEXT_PUBLIC_YANDEX_API_KEY
	console.log(apiKey)

	return (
		<>
			<YMaps query={{ apikey: apiKey }}>
				<QueryClientProvider client={queryClient}>
					{children}
				</QueryClientProvider>
			</YMaps>
			<ReactQueryDevtools client={queryClient} initialIsOpen={false} />
		</>
	)
}