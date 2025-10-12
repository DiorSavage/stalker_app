"use client"
import Image from 'next/image'
import Script from 'next/script'
import { useEffect, useRef, useState } from 'react'
import { Map, Placemark, useYMaps } from '@pbe/react-yandex-maps';
import { YMapsApi } from '@pbe/react-yandex-maps/typings/util/typing'
import { Portal } from './Portal'
import { UserMarkerLayout } from './UserMarkerLayout'

interface IGeoParams {
	latitude: number;
	longitude: number;
}

export default function MapHomeComponent() {

	const [currentGeo, setCurrentGeo] = useState<IGeoParams>({ latitude: 0, longitude: 0 })
	const [centerPosition, setCenterPosition] = useState<IGeoParams>({ latitude: 55.645862, longitude: 37.581191 })
	const apiKey = process.env.NEXT_PUBLIC_YANDEX_API_KEY
	const [activePortal, setActivePortal] = useState<boolean>(false)

	useEffect(() => {
		if (!navigator.geolocation) {
			console.log("Geolocation is not supported by your browser");
			return;
		}

		navigator.geolocation.getCurrentPosition(
			(position) => {
				console.log("Latitude:", position.coords.latitude);
				console.log("Longitude:", position.coords.longitude);
				setCurrentGeo({
					latitude: position.coords.latitude,
					longitude: position.coords.longitude,
				});
				console.log(currentGeo)
			},
			(err) => {
				console.error("Error getting geolocation:", err);
			},
			{
				timeout: 10000,
				maximumAge: 60000,
				enableHighAccuracy: true,
			}
		);
	}, []);

	useEffect(() => {
		setCenterPosition({
			latitude: currentGeo.latitude,
			longitude: currentGeo.longitude,
		});
	}, [currentGeo])

	return (
		<>
			<h1 className=''>Карта друзей</h1>
			<div className="w-full h-[800px]">
				<Map
					defaultState={{
						center: [currentGeo.latitude, currentGeo.longitude],
						zoom: 15,
					}}
					width="100%"
					modules={[ "geoObject.addon.balloon", "geoObject.addon.hint" ]}
					height="100%"
				>
					<Placemark
            geometry={[currentGeo.latitude, currentGeo.longitude]}
            // options={{
						// 	iconImageHref: "/assets/user_default_icon.png",
            //   iconLayout: customLayoutRef.current || 'default#image',
            //   iconImageSize: [30, 30],
            //   iconImageOffset: [-15, -30],
            // }}
						options={{
							preset: "islands#circleIcon",
							iconColor: "#ffffff",
							hasHint: true,
							draggable: false,
							openHintOnHover: true,
							// balloonContent: "<div id='current_user_icon' class='w-[240px] h-[400px]></div>",
						}}
						properties={{
							iconContent: "<img src='/assets/user_default_icon.png' class='w-[40px] aspect-square'></img>",
							hintContent: "<b>Nigger churka</b>",
							balloonContent: "<div id='current_user_icon' class='w-[240px] h-[400px]'></div>"
						}}
						onClick={
							() => {
								setTimeout(() => {
									setActivePortal(true)
								}, 0);
							}
						}
          />
				</Map>
				{ activePortal && <Portal elementId='current_user_icon'>
					<UserMarkerLayout imageUrl='/assets/user_default_icon.png' />
				</Portal> }
			</div>
		</>
	)
}