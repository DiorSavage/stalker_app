"use client"

import MapHomeComponent from '@/app/_components/Maps/MapHomeComponent'
import dynamic from 'next/dynamic'
import { Suspense } from "react";

const MapComponent = dynamic(async () => import("@/app/_components/Maps/MapHomeComponent"), {
  ssr: false,
  loading: () => <p>Загрузка карты...</p>,
});

export default function HomePage() {

  return (
		<>
			<section className='w-page h-full flex flex-col items-center gap-y-4'>
				{/* <Suspense fallback={<div>Loading...</div>}>
					<MapComponent />
				</Suspense> */}
				<MapComponent />
			</section>
		</>
  );
}