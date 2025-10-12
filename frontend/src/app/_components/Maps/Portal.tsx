import { useEffect } from 'react'
import { createPortal } from 'react-dom'

export const Portal = ({ children, elementId }: { children: React.ReactNode, elementId: string }) => {
	const mount = document.getElementById(elementId) as HTMLDivElement
	const el = document.createElement("div")

	useEffect(() => {
		if (mount) mount.appendChild(el)
		return () => {
			if (mount) mount.removeChild(el)
		}
	}, [el, mount])

	if (!mount) return null

	return createPortal(children, el)
}