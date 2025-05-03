/*
  api.js - Axios API service for Jam-Date frontend
  Handles base URL, JWT injection, error handling, and logging for all API requests.
*/

import axios from 'axios'

/**
 * Create an Axios instance with base configuration.
 */
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add JWT token to headers
api.interceptors.request.use(
  (config) => {
    // Do not add token for login or register
    if (!['/auth/login', '/auth/register', '/register'].some((url) => config.url.endsWith(url))) {
      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
    }
    return config
  },
  (error) => {
    console.error('API request error:', error)
    return Promise.reject(error)
  },
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error('API response error:', error.response.data)
    } else {
      console.error('API error:', error.message)
    }
    return Promise.reject(error)
  },
)

export default api
