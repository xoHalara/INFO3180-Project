/*
  profile.js - Pinia store for Jam-Date profile and favourites state management
  Handles fetching, searching, and managing profiles, favourites, and matches.
*/

import { defineStore } from 'pinia'
import {
  fetchAllProfiles,
  fetchLastProfiles,
  fetchProfileById,
  addProfile,
  searchProfiles,
  favouriteProfile,
  getProfileMatches,
  getUserFavourites,
  getTopFavourites,
} from '../api/profile'

/**
 * Store for managing profiles, favourites, and matches.
 */
export const useProfileStore = defineStore('profile', {
  state: () => ({
    profiles: [],
    lastProfiles: [],
    searchResults: [],
    profileDetails: null,
    favourites: [],
    topFavourites: [],
    matches: [],
    loading: false,
    error: null,
  }),

  actions: {
    /**
     * Fetch all profiles.
     */
    async loadAllProfiles() {
      this.loading = true
      this.error = null
      try {
        const res = await fetchAllProfiles()
        this.profiles = res.data
      } catch (err) {
        this.error = err
      } finally {
        this.loading = false
      }
    },

    /**
     * Fetch the last N profiles (default 4).
     */
    async loadLastProfiles(n = 4) {
      this.loading = true
      this.error = null
      try {
        const res = await fetchLastProfiles(n)
        this.lastProfiles = res.data
      } catch (err) {
        this.error = err
      } finally {
        this.loading = false
      }
    },

    /**
     * Fetch a profile by ID.
     */
    async loadProfileDetails(profileId) {
      this.loading = true
      this.error = null
      try {
        const res = await fetchProfileById(profileId)
        this.profileDetails = res.data
      } catch (err) {
        this.error = err
      } finally {
        this.loading = false
      }
    },

    /**
     * Add a new profile.
     */
    async createProfile(profileData) {
      this.loading = true
      this.error = null
      try {
        await addProfile(profileData)
        await this.loadAllProfiles()
      } catch (err) {
        this.error = err
      } finally {
        this.loading = false
      }
    },

    /**
     * Search for profiles by criteria.
     */
    async searchProfilesAction(params) {
      this.loading = true
      this.error = null
      try {
        const res = await searchProfiles(params)
        this.searchResults = res.data
      } catch (err) {
        this.error = err
      } finally {
        this.loading = false
      }
    },

    /**
     * Mark a profile as favourite for the logged-in user.
     */
    async favouriteProfileAction(userId, favUserId) {
      this.loading = true
      this.error = null
      try {
        await favouriteProfile(userId, favUserId)
        await this.loadFavourites(userId)
      } catch (err) {
        this.error = err
      } finally {
        this.loading = false
      }
    },

    /**
     * Get matches for a profile by ID.
     */
    async loadMatches(profileId) {
      this.loading = true
      this.error = null
      try {
        const res = await getProfileMatches(profileId)
        this.matches = res.data
      } catch (err) {
        this.error = err
      } finally {
        this.loading = false
      }
    },

    /**
     * Get all users favoured by a user.
     */
    async loadFavourites(userId) {
      this.loading = true
      this.error = null
      try {
        const res = await getUserFavourites(userId)
        this.favourites = res.data
      } catch (err) {
        this.error = err
      } finally {
        this.loading = false
      }
    },

    /**
     * Get the top N most favoured users.
     */
    async loadTopFavourites(n = 20) {
      this.loading = true
      this.error = null
      try {
        const res = await getTopFavourites(n)
        this.topFavourites = res.data
      } catch (err) {
        this.error = err
      } finally {
        this.loading = false
      }
    },
  },
})
