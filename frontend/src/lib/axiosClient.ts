import axios from 'axios'

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "localhost:8000"

export const axiosClient = axios.create({
	baseURL: BASE_URL,
	withCredentials: true,
	headers: {
		"Content-Type": "application/json",
	}
})