"use client"

import clsx from 'clsx'
import { useState } from 'react'

export default function Sidebar() {

	const [isOpened, setIsOpened] = useState<boolean>(true)

	return (
		<div className={clsx("flex flex-col items-center h-full", isOpened ? "w-side-desktop" : "w-side-hidden")}></div>
	)
}