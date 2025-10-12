"use client"

import Image from 'next/image'
import Link from 'next/link'
import { useState } from 'react'

export default function Header() {

	const [burgerOpen, setBurgerOpen] = useState<boolean>(false)

	return (
		<header className="flex items-center justify-between h-[10vh] w-full xl:w-page bg-white px-12 xl:rounded-b-2xl text-gray-900">
			<div onClick={() => setBurgerOpen(!burgerOpen)} className={`burger-menu ${burgerOpen && "burger-active"}`}></div>
			<Image className='cursor-pointer' src={"/assets/app_icon.png"} width={60} height={60} alt='App Icon' />
			<div className="hidden md:flex items-center justify-between w-2/3 lg:w-1/3">
				{['/map', '/friends', "/chats", '/posts', '/subscription'].map((href, i) => (
					<Link
						key={i}
						href={href}
						className="text-blue-500 hover:text-blue-700 hover:bg-[#0000001c] transition-all duration-300 py-1 px-2 rounded-md"
					>
						{['Карта', 'Друзья', "Чаты", 'Посты', 'Подписка'][i]}
					</Link>
				))}
			</div>
			<button className="px-8 py-2.5 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors cursor-pointer">
				Войти
			</button>
		</header>
	)
}