/*
  favourite.js - Pinia store for managing favouriting logic and feedback UI
  Centralizes favouriting API calls and per-profile feedback state for reuse across the app.
*/

import { defineStore } from 'pinia'
import api from '../api/api'

export const useFavouriteStore = defineStore('favourite', {
  state: () => ({
    favStates: {}, // { [profileId]: { loading, success, error } }
  }),

  actions: {
    /**
     * Favourite a profile for the current user.
     * @param {string|number} profileUserId - The user_id of the profile to favourite
     * @returns {Promise<void>}
     */
    async favouriteProfile(profileUserId) {
      if (!profileUserId) return
      this.favStates[profileUserId] = { loading: true, success: false, error: '' }
      try {
        await api.post(`/profiles/${profileUserId}/favourite`, {})
        this.favStates[profileUserId] = { loading: false, success: true, error: '' }
        setTimeout(() => {
          this.favStates[profileUserId] = { loading: false, success: false, error: '' }
        }, 2000)
      } catch (err) {
        this.favStates[profileUserId] = {
          loading: false,
          success: false,
          error: err.response?.data?.message || 'Failed to add to favourites.',
        }
      }
    },
    /**
     * Reset feedback state for a profile.
     */
    resetFavState(profileUserId) {
      this.favStates[profileUserId] = { loading: false, success: false, error: '' }
    },
  },
})
