/*
  profile.js - API service for Jam-Date profile-related endpoints
  Provides functions for fetching, searching, and managing profiles and favourites.
*/

import api from './api'

/**
 * Fetch all profiles.
 */
export const fetchAllProfiles = () => api.get('/profiles/')

/**
 * Fetch the last N profiles (default 4).
 */
export const fetchLastProfiles = (n = 4) => api.get(`/profiles/?limit=${n}`)

/**
 * Fetch a profile by its ID.
 */
export const fetchProfileById = (profileId) => api.get(`/profiles/${profileId}`)

/**
 * Add a new profile.
 */
export const addProfile = (profileData) => api.post('/profiles/', profileData)

/**
 * Search for profiles by criteria.
 */
export const searchProfiles = (params) => api.get('/search/', { params })

/**
 * Mark a profile as favourite for the logged-in user.
 */
export const favouriteProfile = (userId, favUserId) =>
  api.post(`/profiles/${userId}/favourite`, { fav_user_id: favUserId })

/**
 * Get matches for a profile by ID.
 */
export const getProfileMatches = (profileId) => api.get(`/profiles/matches/${profileId}`)

/**
 * Get all users favoured by a user.
 */
export const getUserFavourites = (userId) => api.get(`/users/${userId}/favourites`)

/**
 * Get the top N most favoured users.
 */
export const getTopFavourites = (n = 20) => api.get(`/users/favourites/${n}`)
