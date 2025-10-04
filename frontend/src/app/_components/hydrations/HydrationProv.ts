"use server"

import { queryClient } from '@/lib/queryClient'
import { dehydrate, HydrationBoundary } from '@tanstack/react-query'

// async function getHydratedState() {
// 	queryClient.prefetchQuery({
// 		queryKey: ["mydata"],
// 		queryFn: getMe,
// 		staleTime: Infinity,
// 		gcTime: Infinity,
// 		retry: false
// 	})

// 	return { dehydratedState: dehydrate(queryClient) }
// }

// export async function HydrationProv({ children }: { children: React.ReactNode }) {
// 	const { dehydratedState } = await getHydratedState()

// 	return (
// 		<HydrationBoundary state={dehydratedState}>
// 			{children}
// 		</HydrationBoundary>
// 	)
// }